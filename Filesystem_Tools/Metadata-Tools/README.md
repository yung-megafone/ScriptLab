# Metadata Tools

## Overview
The **Metadata Tools** collection provides utilities for extracting, modifying, and embedding metadata into media files. These tools help organize and structure digital libraries by ensuring files contain accurate metadata based on their filenames or external sources.

## 📂 Tools Included

### **1️⃣ Metadata Writer (Filename to Metadata)**
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

### **2️⃣ Future Tools**
🚀 **Coming soon:** Additional tools for fetching and organizing metadata from online sources.

## 🛠 Installation
To install dependencies, run:
```bash
pip install -r ../../requirements.txt
```

## 📜 License
This project is licensed under the **MIT License**. See [LICENSE](../../LICENSE) for details.