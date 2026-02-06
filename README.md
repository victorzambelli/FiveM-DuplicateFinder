# 🔍 FiveM-DuplicateFinder

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()

A GUI tool for finding and removing duplicate asset files between two folders.

**Built for FiveM/RedM developers** to clean up animations, models, types, and collision files.

---

## ✨ Features

- 📂 Compare two folders for duplicate files
- 🔎 Filter by file extensions (`.ycd`, `.ydr`, `.ytyp`, `.ybn`)
- 📋 View detailed list of duplicates found
- 🗑️ Safe deletion - files moved to Recycle Bin (recoverable)
- 🌐 Multi-language support (English / Português)
- 💻 Simple and intuitive interface

---

## 📥 Installation

### Option 1: Run with Python

```bash
# Clone the repository
git clone https://github.com/victorzambelli/FiveM-DuplicateFinder.git
cd FiveM-DuplicateFinder

# Install dependencies
pip install send2trash

# Run the application
python duplicate_finder.py
```

### Option 2: Download Executable

Download the latest release from [Releases](https://github.com/victorzambelli/FiveM-DuplicateFinder/releases) and run `DuplicateFinder.exe`.

---

## 🎮 Supported Extensions

| Extension | Description |
|-----------|-------------|
| `.ycd` | Animation files (Clip Dictionary) |
| `.ydr` | 3D model files (Drawable) |
| `.ytyp` | Type definition files (Archetype) |
| `.ybn` | Collision files (Bounds) |

---

## 🚀 How to Use

1. **Select Folder 1** - First folder to compare
2. **Select Folder 2** - Second folder to compare
3. **Choose extensions** - Check which file types to scan
4. **Click "Scan for Duplicates"** - Start the comparison
5. **Select deletion source** - Choose which folder to remove duplicates from
6. **Click "Move to Recycle Bin"** - Safely remove duplicates

> ⚠️ Files are moved to the Recycle Bin and can be restored if needed.

---

## 🛠️ Build Executable

To create a standalone `.exe` file:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name DuplicateFinder duplicate_finder.py
```

The executable will be created in the `dist/` folder.

---

## 📋 Requirements

- Python 3.8+
- `send2trash` (`pip install send2trash`)
- `tkinter` (included with Python)

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Developed by **Victor Z**

For FiveM/RedM community use.
