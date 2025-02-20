"""
Checksum File Renamer
-----------------------------
Author: yung-megafone
Date: 2025-02-17
License: MIT License

Description:
This script scans a directory for files and renames them based on their SHAKE-128 checksum.
If a file with the same checksum-based name already exists, the duplicate is removed.

Features:

Computes SHAKE-128 checksums efficiently for all files.

Renames files using their checksum while preserving original file extensions.

Automatically removes duplicate files with the same checksum.

Utilizes multithreading to improve performance.

Allows customizable checksum length (default: 12 bytes).

Usage:
python checksum-rename.py <directory_path>

The script prompts for the checksum length (default: 12 bytes) before processing files.

Example:
python checksum-rename.py /path/to/directory
Enter checksum filename length (default: 12): 16

This will rename all files in /path/to/directory using a 16-byte SHAKE-128 checksum.

Notes:

If a file is already named according to its checksum, it will be skipped.

If a renamed file already exists, the original file is deleted to prevent duplicates.

The script utilizes threading to enhance processing speed.

"""
import hashlib
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm  # Progress bar

def calculate_shake128_checksum(file_path: str, digest_length: int = 12) -> str:
    """
    Computes the SHAKE-128 checksum of the specified file.

    :param file_path: Absolute path of the file to compute checksum for.
    :param digest_length: Number of bytes for the SHAKE-128 digest (default: 12).
    :return: Hexadecimal SHAKE-128 checksum string.
    """
    shake128_hasher = hashlib.shake_128()
    
    # Read file in chunks to efficiently process large files
    with open(file_path, 'rb') as file:
        while chunk := file.read(128 * 1024):  # 128 KB buffer
            shake128_hasher.update(chunk)
    
    return shake128_hasher.hexdigest(digest_length)

def rename_file_to_checksum(file_path: str, digest_length: int = 12) -> None:
    """
    Renames a file using its SHAKE-128 checksum.

    - If a file with the same checksum-based name already exists, the original file is deleted.
    - If the file is already named correctly, no action is taken.

    :param file_path: Absolute path of the file to rename.
    :param digest_length: Number of bytes for the SHAKE-128 digest (default: 12).
    """
    file_directory = os.path.dirname(file_path)
    file_extension = os.path.splitext(file_path)[1]  # Preserve file extension

    checksum = calculate_shake128_checksum(file_path, digest_length)
    new_filename = f"{checksum}{file_extension}"
    new_file_path = os.path.join(file_directory, new_filename)

    # If the file is already named correctly, do nothing
    if os.path.basename(file_path) == new_filename:
        return

    # If a file with the target name exists, delete the current file
    if os.path.exists(new_file_path):
        os.remove(file_path)
    else:
        os.rename(file_path, new_file_path)

def process_files_in_directory(directory_path: str, digest_length: int = 12) -> None:
    """
    Processes all files in the specified directory by renaming them using their SHAKE-128 checksum.

    - Utilizes a ThreadPoolExecutor for concurrent execution.
    - Skips directories, only processing regular files.

    :param directory_path: Path to the target folder containing files to process.
    :param digest_length: Number of bytes for the SHAKE-128 digest (default: 12).
    """
    file_list = []

    # Collect all files in the directory
    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_list.append(os.path.join(root, filename))

    if not file_list:
        print("No files found in the specified directory.")
        return

    # Use tqdm progress bar while processing files
    with ThreadPoolExecutor() as executor:
        list(tqdm(executor.map(rename_file_to_checksum, file_list, [digest_length] * len(file_list)), 
                  total=len(file_list), desc="Renaming Files", unit="file"))

def main() -> None:
    """
    Main function.

    - Accepts a directory path as a command-line argument.
    - Prompts for filename checksum length (default: 12).
    - Processes each file within the directory to rename them based on SHAKE-128 checksum.
    """
    if len(sys.argv) < 2:
        print("Usage: python checksum-rename.py <directory_path>")
        sys.exit(1)

    target_directory = sys.argv[1]

    if not os.path.isdir(target_directory):
        print(f"Error: '{target_directory}' is not a valid directory.")
        sys.exit(1)
    
    # Prompt user for checksum length with default value of 12
    try:
        digest_length = int(input("Enter checksum filename length (default: 12): ") or 12)
    except ValueError:
        print("Invalid input. Using default length of 12.")
        digest_length = 12
    
    process_files_in_directory(target_directory, digest_length)

if __name__ == '__main__':
    main()