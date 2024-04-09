import json
import requests
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from itertools import cycle
from tkinter import Tk, filedialog, StringVar, OptionMenu, Toplevel
from tkinter.ttk import Style, Label, Entry, Button, Progressbar
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

language_map = {
    'Arabic': 'AR',
    'Bulgarian': 'BG',
    'Czech': 'CS',
    'Danish': 'DA',
    'German': 'DE',
    'Greek': 'EL',
    'English': 'EN',
    'Spanish': 'ES',
    'Estonian': 'ET',
    'Finnish': 'FI',
    'Chinese (simplified)': 'ZH'
}

endpoints = [
    'https://api.deeplx.org/translate',
    'https://deeplxpro.vercel.app/translate',
    'https://deeplx.llleman.com/translate',
    'https://deeplx.papercar.top/translate',
    'https://dlx.bitjss.com/translate',
    'https://deeplx.ychinfo.com/translate',
    'https://free-deepl.speedcow.top/translate',
    'https://deepx.dumpit.top/translate',
    'https://deepl.wuyongx.uk/translate',
    'https://deeplx.he-sb.top/translate',
    'https://deepl.aimoyu.tech/translate',
    'https://deepl.tr1ck.cn/translate',
    'https://translate.dftianyi.com/translate',
]

endpoints_cycle = cycle(endpoints)

def preserve_tags(text):
    tags = re.findall(r'<[^>]+>', text)
    for i, tag in enumerate(tags):
        text = text.replace(tag, f"{{TAG{i}}}")
    return text, tags

    
def translate_text(text, source_lang, target_lang, max_retries=5):
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({
        'text': text,
        'source_lang': source_lang,
        'target_lang': target_lang
    })
    retries = 0

    while retries < max_retries:
        url = next(endpoints_cycle)
        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            if response.status_code == 200:
                return response.json()['data']
            else:
                print(f"连接错误，状态码: {response.status_code} - {response.text}，正在重试...")
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}，正在重试...")
        retries += 1
        time.sleep(1)  

    print(f"节点翻译失败，已达到最大重试次数: {max_retries}")
    return None


def translate_xml_file(file_path, source_lang, target_lang):
    tree = ET.parse(file_path)
    root = tree.getroot()

    text_nodes = [node for node in root.iter() if node.text and not node.text.isspace()]
    total_nodes = len(text_nodes)

    progress_window = Toplevel()
    progress_window.title('翻译进度')
    progress_var = StringVar(progress_window, '0%')
    progress_label = Label(progress_window, textvariable=progress_var)
    progress_label.pack()
    progress_bar = Progressbar(progress_window, orient='horizontal', length=300, mode='determinate', maximum=total_nodes)
    progress_bar.pack(pady=10)
    progress_window.update()

    def translate_node(node):
        if node.text:
            preserved_text, tags = preserve_tags(node.text)
            translated_text = None
            while translated_text is None:
                try:
                    translated_text = translate_text(preserved_text, source_lang, target_lang)
                except Exception as e:
                    print(f"翻译节点文本时出现异常: {e}，正在重试...")
                    time.sleep(1)
            for i, tag in enumerate(tags):
                translated_text = translated_text.replace(f"{{TAG{i}}}", tag)
            node.text = translated_text
            progress_bar['value'] += 1
            progress_var.set(f'翻译进度: {progress_bar["value"]}/{total_nodes} ({(progress_bar["value"]/total_nodes)*100:.2f}%)')
            progress_window.update_idletasks()

    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(translate_node, node) for node in text_nodes]
        for future in futures:
            future.result()

    new_file_path = Path(file_path).stem + f"_{target_lang}.xml"
    tree.write(new_file_path, encoding='utf-8', xml_declaration=True)

    progress_window.destroy()
    return new_file_path

class TranslationGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('XML翻译器')

        self.style = Style()
        self.style.theme_use('clam')
        self.style.configure('TLabel', font=('Arial', 12), background='white')
        self.style.configure('TEntry', font=('Arial', 12))
        self.style.configure('TButton', font=('Arial', 12), background='lightblue')

        self.label_file_path = Label(master, text='XML文件路径:', style='TLabel')
        self.label_file_path.grid(row=0, column=0, padx=10, pady=10)
        self.entry_file_path = Entry(master, style='TEntry')
        self.entry_file_path.grid(row=0, column=1, padx=10, pady=10)
        self.button_browse = Button(master, text='浏览', command=self.browse_file, style='TButton')
        self.button_browse.grid(row=0, column=2, padx=10, pady=10)

        self.source_lang_var = StringVar(master)
        self.source_lang_var.set('English')
        self.option_menu_source_lang = OptionMenu(master, self.source_lang_var, *language_map.keys())
        self.option_menu_source_lang.grid(row=1, column=1, padx=10, pady=10)

        self.target_lang_var = StringVar(master)
        self.target_lang_var.set('Chinese (simplified)')
        self.option_menu_target_lang = OptionMenu(master, self.target_lang_var, *language_map.keys())
        self.option_menu_target_lang.grid(row=2, column=1, padx=10, pady=10)

        self.button_translate = Button(master, text='翻译', command=self.start_translation_thread, style='TButton')
        self.button_translate.grid(row=3, column=1, padx=10, pady=10)

        self.label_result = Label(master, text='', style='TLabel')
        self.label_result.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
    
    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.entry_file_path.delete(0, 'end')
        self.entry_file_path.insert(0, file_path)

    def start_translation_thread(self):
        translation_thread = Thread(target=self.translate)
        translation_thread.start()

    def translate(self):
        file_path = self.entry_file_path.get()
        source_lang = language_map[self.source_lang_var.get()]  
        target_lang = language_map[self.target_lang_var.get()]  
        try:
            translated_file_path = translate_xml_file(file_path, source_lang, target_lang)
            self.label_result.config(text=f'翻译后的XML文件已保存为 {translated_file_path}')
        except Exception as e:
            self.label_result.config(text=str(e))

root = Tk()
gui = TranslationGUI(root)
root.mainloop()