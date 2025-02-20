# Metadata Writer (Filename to Metadata)

## Overview
The **Metadata Writer** is a script that extracts **structured metadata from filenames** and embeds it into the **audio file’s metadata tags**. This helps standardize metadata for better organization in media players and digital libraries.

## Features
✅ **Extracts metadata from filenames** (Track Number, Artist, Title, Featured Artists).  
✅ **Supports MP3, FLAC, and WAV formats**.  
✅ **Handles inconsistently formatted filenames**.  
✅ **Recognizes various feature artist conventions (`feat.`, `ft.`, `featuring`)**.  
✅ **Uses `mutagen` to modify metadata tags**.  
✅ **Includes a progress bar for large collections**.  

## Installation
To install dependencies, run:
```bash
pip install -r ../../requirements.txt
```

## Usage
Run the script with the directory containing music files:
```bash
python meta-write.py /path/to/music
```

## Example
### **Before Running the Script:**
```
📂 Music/
├── 01 - Drake - God's Plan.mp3
├── 02 - Kanye West_Flash Lights.mp3
└── Travis Scott - HIGHEST IN THE ROOM feat. Lil Baby.mp3
```

### **After Running the Script:**
The metadata inside the files will now be properly structured:
- **Track Number:** `01`  
- **Artist:** `Drake`  
- **Title:** `God's Plan`  
- **Featured Artists:** _(if applicable)_  

## License
This project is licensed under the **MIT License**. See [LICENSE](../../LICENSE) for details.