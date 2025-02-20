# Checksum File Renamer

## Overview
The **Checksum File Renamer** is a Python script that scans a directory for files and renames them based on their **SHAKE-128 checksum**. If a file with the same checksum-based name already exists, the duplicate is automatically removed.

## Features
✅ **Computes SHAKE-128 checksums efficiently for all files.**  
✅ **Renames files using their checksum while preserving original file extensions.**  
✅ **Automatically removes duplicate files with the same checksum.**  
✅ **Utilizes multithreading (`ThreadPoolExecutor`) for improved performance.**  
✅ **Allows customizable checksum length (default: 12 bytes).**  
✅ **Uses a progress bar (`tqdm`) for real-time tracking of file renaming.**  

## Installation
To install dependencies, run:
```bash
pip install -r requirements.txt
```

## Usage
Run the script with the target directory:
```bash
python checksum-rename.py /path/to/directory
```

### **Specify a Custom Checksum Length**
You can specify a custom SHAKE-128 length (default: 12 bytes) when prompted:
```bash
python checksum-rename.py /path/to/directory
Enter checksum filename length (default: 12): 16
```

## Example Output
```
Renaming Files:  45% | ██████       | 45/100 [00:03<00:02, 22.00 files/s]
```

## Implementation Details
- **Reads files in chunks (128 KB)** to efficiently compute SHAKE-128 hashes.  
- **Utilizes `ThreadPoolExecutor`** for concurrent file renaming.  
- **Prevents renaming files already named according to their checksum.**  
- **Deletes duplicate files if a renamed file already exists.**  
- **Progress bar (`tqdm`) for real-time status updates.**  

## License
This project is licensed under the **MIT License**. See [LICENSE](../LICENSE) for details.

## Future Improvements
🔹 **Support for additional hashing algorithms (SHA-256, MD5, etc.).**  
🔹 **Option to move renamed files to a separate folder.**  
🔹 **Error handling for locked or inaccessible files.**  

For feature requests or contributions, feel free to open an **issue** or **pull request**! 🚀