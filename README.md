# AutoFile Pro 📂

**AutoFile Pro** is a smart, automated file management system built with Python and CustomTkinter. It helps users organize cluttered directories, automate backups, and clean up storage based on file age or size constraints.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-green)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Features

### 1. 🗂️ Intelligent Organizer
Sorts files into subfolders automatically based on three modes:
- **By Extension:** Groups files into Documents, Images, Videos, Code, etc.
- **By Size:** categorizes into Small, Large, and Very Large folders (thresholds configurable).
- **By Age:** Separates Recent, Old, and Very Old files based on modification date.

### 2. 💾 Smart Backup
- Creates full backups of specified directories.
- **Compression Support:** Optional `.zip` compression to save space.
- Threaded execution ensures the GUI never freezes during large file copies.

### 3. 🧹 Cleanup Tool
Helps free up disk space by identifying files matching specific criteria:
- **Mode:** Filter by **Size** (MB) or **Age** (Days).
- **Actions:** Safely move files to a **Recycle Bin** or an **Archive** folder.

### 4. ⚙️ Dynamic Configuration
- **Settings Dashboard:** Adjust thresholds (e.g., what counts as "Old" or "Large") directly from the GUI.
- **Persistence:** All preferences are saved automatically to `autofile.toml`.
- **Safety:** "Protected Directory" logic ensures system folders or organized folders are never touched.

## 🛠️ Tech Stack
- **Frontend:** `CustomTkinter` (Modern, Dark-mode native GUI).
- **Backend:** Python `pathlib`, `shutil`, `threading`.
- **Config:** `TOML` based configuration management.
- **Safety:** `Send2Trash` for safe deletion.

## 📦 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/fatehali1122/AutoFile-Pro.git
   cd AutoFilePro
   Create a Virtual Environment (Recommended)

2. **Create a Virtual Environment (Recommended)**
    ```bash
   python -m venv .venv
   ```
   - On Windows:  
     ```powershell
     .venv\Scripts\activate
     ```
   - On macOS/Linux:  
     ```bash
     source .venv/bin/activate
     ```
3. **Install Dependencies**

   ```bash
    pip install -r requirements.txt
4. **Run the Application**
   ```bash
    python MainApp.py
## ⚙️ Configuration
- The app generates an autofile.toml file on the first run.
- You can modify settings via the Settings Tab in the app or by editing this file directly.

## ✅ Requirements
- Python 3.10+  
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [Send2Trash](https://pypi.org/project/Send2Trash/)

## 👨‍💻 Author
Made by **Fateh Ali**  
[LinkedIn](https://www.linkedin.com/in/fateh-ali-072348352/) | [GitHub](https://github.com/fatehali1122)  

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

- This project is for educational and productivity purposes only.
- Always double-check files before running the Cleanup tool.
- The author is not responsible for any accidental data loss caused by misuse of the "Delete" or "Recycle Bin" functions.
