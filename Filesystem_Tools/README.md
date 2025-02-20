# Filesystem Tools

## Overview
The **Filesystem Tools** collection contains scripts designed to help manage and organize files and folders efficiently. These tools simplify file renaming, directory structure visualization, and folder customization.

## 📂 Tools Included

### **1️⃣ Directory Structure Generator**
📌 **Generates an ASCII directory tree of a folder and its subdirectories.**
- Displays a full folder tree with file sizes.
- Supports **JSON output**.
- Allows excluding specific folders or file types.
- Uses a progress bar for tracking large structures.

📍 **Usage:**
```bash
python dir-structure.py /path/to/folder --json
```

---

### **2️⃣ Icon Changer**
📌 **Assigns a custom folder icon to all subdirectories.**
- Supports Windows (`.ico` files).
- Includes **recursive mode** to process all subfolders.
- Uses `desktop.ini` to apply icons without restarting Explorer.

📍 **Usage:**
```bash
python icon-changer.py /path/to/folders /path/to/icon.ico --recursive
```

---

### **3️⃣ File Renamers**

#### ✅ **Checksum File Renamer**
📌 **Renames files using their SHAKE-128 checksum.**
- Prevents duplicates by ensuring unique names.
- Uses **multithreading** for faster processing.
- Includes a progress bar for better tracking.

📍 **Usage:**
```bash
python checksum-rename.py /path/to/files
```

#### ✅ **Music File Renamer**
📌 **Renames music files based on metadata (ID3, FLAC, WAV tags).**
- Formats filenames as `01 - Artist - Song Title.mp3`.
- Supports **recursive processing** of subdirectories.
- Prevents overwriting and allows moving renamed files.

📍 **Usage:**
```bash
python music-renamer.py /path/to/music --copy
```

---

### **4️⃣ Metadata Writer (Filename to Metadata)**
📌 **Extracts structured information from filenames and writes it as embedded metadata.**
- Supports **MP3, FLAC, and WAV** formats.
- Parses filenames for **Track Number, Artist, Title, and Featured Artists**.
- Handles **inconsistent file naming conventions**.
- Uses **Mutagen** to modify metadata tags.
- Includes a **progress bar** for large collections.

📍 **Usage:**
```bash
python meta-write.py /path/to/music
```

## 🛠 Installation
To install dependencies, run:
```bash
pip install -r ../../requirements.txt
```

## 📜 License
This project is licensed under the **MIT License**. See [LICENSE](../../LICENSE) for details.