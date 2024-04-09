# XML Machine Translator

This is a simple XML translator written in Python that can help you translate text within XML files from one language to another.

The initial intent of this project was to localize the files for "Baldur's Gate 3"'s mods, but it may not fully support other XML files. Future maintenance will be considered based on issues, and contributions via Pull Requests to make this a more complete XML translation tool are welcome.

## Features

- Supports translation between multiple languages.
- Uses a loop to switch between multiple translation API nodes to increase the success rate of translations.
- Provides a Graphical User Interface (GUI) for users to select files and translation languages.
- Uses a thread pool to speed up the translation process.
- Displays translation progress.

## How to Use

***Method 1: Compile Yourself***
1. Clone the repository to your local machine.
2. Install the required dependencies using `pip installer -r requirements.txt`.
3. Run the `app.py` file.
4. In the GUI, select your XML file and translation language.
5. Click the translate button to start translating.

***Method 2: Use the Released .exe***
1. Download from the release distribution.
2. Double-click the .exe file.
3. In the GUI, select your XML file and translation language.
4. Click the translate button to start translating.

## Dependencies

- Python 3
- requests
- tkinter
- concurrent

## Contributions

Contributions via Pull Requests or Issues are welcome.

## Acknowledgments

Special thanks to OwO-Network/DeepLX for their support.

## License

MIT
