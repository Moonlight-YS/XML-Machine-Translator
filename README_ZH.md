# XML机器翻译器

这是一个使用Python编写的简单XML翻译器，它可以帮助您将XML文件中的文本从一种语言翻译成另一种语言。

本项目初衷是为了汉化《博德之门3》模组的本地化文件，其他xml文件支持但是功能可能不会很齐全，未来可能会根据issue酌情进行维护，同时欢迎各位进行PR使项目变成更加完善的xml翻译工具

## 功能

- 支持多种语言之间的翻译。
- 使用循环的方式在多个翻译API节点之间切换，以提高翻译成功率。
- 提供图形用户界面（GUI），方便用户选择文件和翻译语言。
- 使用线程池来加速翻译过程。
- 显示翻译进度。

## 如何使用
***一.自行编译***
1. 克隆仓库到本地。
2. 使用```pip installer -r requirements.txt```安装所需的依赖。
3. 运行`app.py`文件。
4. 在GUI中选择您的XML文件和翻译语言。
5. 点击翻译按钮开始翻译。

***二.使用release分发exe***
1. 在分发中下载。
2. 双击exe。
3. 在GUI中选择您的XML文件和翻译语言。
4. 点击翻译按钮开始翻译。
## 依赖

- Python 3
- requests
- tkinter
- concurrent

## 贡献

欢迎通过Pull Requests或Issues来贡献您的代码或提出建议。


同时感谢OwO-Network/DeepLX(https://github.com/OwO-Network/DeepLX)项目提供的翻译服务来源
## 许可证

MIT
