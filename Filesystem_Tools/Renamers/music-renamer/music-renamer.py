"""
Music File Renamer
-----------------------------
Author: yung-megafone
Date: 2025-02-18
License: MIT License

Description:
This script automatically renames music files based on their metadata.
It extracts track number, title, artist, and featured artists (if available), then renames the files accordingly.

Features:

Supports MP3, FLAC, and WAV formats.

Formats filenames as: "01 - Artist - Song Title (feat. Featured Artist).mp3".

By default, renames files in place.

Use --copy flag to copy renamed files to a "Renamed Music" folder instead.

Prevents overwriting by appending (1), (2), etc., when necessary.

Recursively scans subdirectories for music files.

Usage:
python music_renamer.py <directory_path>

Example:
python music_renamer.py "/Users/YourName/Music"

With --copy flag:
python music_renamer.py "/Users/YourName/Music" --copy

Output Example:
📂 Music/
├── 01 - Artist - Song Title.mp3
├── 02 - Artist - Another Song.mp3
├── 03 - Artist - A Third Song (feat. Featured Artist).mp3

"""
"""
Music File Renamer
-----------------------------
Author: yung-megafone
Date: 2025-02-18
License: MIT License

Description:
This script automatically renames music files based on their metadata.
It extracts track number, title, artist, and featured artists (if available), then renames the files accordingly.

Features:

Supports MP3, FLAC, and WAV formats.

Formats filenames as: "01 - Artist - Song Title (feat. Featured Artist).mp3".

By default, renames files in place.

Use --copy flag to copy renamed files to a "Renamed Music" folder instead.

Prevents overwriting by appending (1), (2), etc., when necessary.

Recursively scans subdirectories for music files.

Usage:
python music_renamer.py <directory_path>

Example:
python music_renamer.py "/Users/YourName/Music"

With --copy flag:
python music_renamer.py "/Users/YourName/Music" --copy

Output Example:
📂 Music/
├── 01 - Artist - Song Title.mp3
├── 02 - Artist - Another Song.mp3
├── 03 - Artist - A Third Song (feat. Featured Artist).mp3

"""
"""
Music File Renamer
-----------------------------
Author: yung-megafone
Date: 2025-02-18
License: MIT License

Description:
This script automatically renames music files based on their metadata.
It extracts track number, title, artist, and featured artists (if available), then renames the files accordingly.

Features:
- Supports MP3, FLAC, and WAV formats.
- Formats filenames as: "01 - Artist - Song Title (feat. Featured Artist).mp3".
- By default, renames files in place.
- Use --copy flag to copy renamed files to a "Renamed Music" folder instead.
- Prevents overwriting by appending (1), (2), etc., when necessary.
- Recursively scans subdirectories for music files.
- Displays a progress bar while renaming files.

Usage:
    python music_renamer.py <directory_path>

Example:
    python music_renamer.py "/Users/YourName/Music"

With --copy flag:
    python music_renamer.py "/Users/YourName/Music" --copy

Output Example:
📂 Music/
├── 01 - Artist - Song Title.mp3
├── 02 - Artist - Another Song.mp3
├── 03 - Artist - A Third Song (feat. Featured Artist).mp3
"""

import os
import re
import glob as fileFinder
import mutagen as metadataAnalyzer
import shutil
import argparse
from tqdm import tqdm  # Progress bar


# Function to obtain all music files within a given directory
def gather_all_music_files(directory: str):
    """ Retrieves all supported music files within the directory (recursively) """
    supported_file_extensions = ["*.mp3", "*.flac", "*.wav"]
    music_files = [file for ext in supported_file_extensions for file in fileFinder.glob(os.path.join(directory, "**", ext), recursive=True)]
    
    return music_files


# Function to extract metadata from music files
def extract_metadata_from_file(file_path):
    """ Extracts metadata from MP3, WAV, and FLAC files with error handling """
    try:
        audio = metadataAnalyzer.File(file_path, easy=True)  # Automatically detects file format

        if not audio:
            tqdm.write(f"Skipping: {file_path} (Unsupported or corrupted file)")
            return None

        metadata = {
            "track_number": audio.get("tracknumber", ["00"])[0].split("/")[0].zfill(2),
            "title": audio.get("title", ["Unknown Title"])[0],
            "artist": audio.get("artist", ["Unknown Artist"])[0],
        }

        # Handle featured artists, if any are in the title
        title = metadata["title"]
        if "feat." in title.lower():
            metadata["featured_artists"] = title.split("feat.")[-1].strip(" ()")
        else:
            metadata["featured_artists"] = ""

        return metadata

    except metadataAnalyzer.mp3.HeaderNotFoundError:
        tqdm.write(f"Skipping: {file_path} (Invalid MP3 file: Can't sync to MPEG frame)")
        return None
    except Exception as e:
        tqdm.write(f"Skipping: {file_path} (Error: {e})")
        return None


# Function to format filenames using extracted metadata
def format_filename(metadata: dict, file_extension: str):
    """ Generates a properly formatted filename based on extracted metadata """
    track = metadata["track_number"].zfill(2)  # Ensures a two-digit track number
    artist = metadata["artist"]
    title = metadata["title"]
    featured = metadata["featured_artists"]

    # Construct the file format
    if featured:
        new_track_name = f"{track} - {artist} - {title} (feat. {featured}){file_extension}"
    else:
        new_track_name = f"{track} - {artist} - {title}{file_extension}"

    return new_track_name


# Function to sanitize filenames
def sanitize_filename(filename: str):
    """ Removes invalid characters from filenames """
    return re.sub(r'[<>:"/\\|?*]', '', filename)  # Remove forbidden characters


# Function to rename files safely while avoiding overwrites
def rename_music_files(file_path: str, new_track_name: str, output_directory: str, copy_files: bool):
    """ Renames the file and moves it to an organized directory """
    new_track_name = sanitize_filename(new_track_name)  # Remove invalid chars
    new_file_path = os.path.join(output_directory, new_track_name) if copy_files else os.path.join(os.path.dirname(file_path), new_track_name)

    # Prevent overwriting by appending (1), (2), etc.
    counter = 1
    while os.path.exists(new_file_path):
        base, ext = os.path.splitext(new_track_name)
        new_file_path = os.path.join(output_directory, f"{base} ({counter}){ext}")
        counter += 1

    # Perform copy or rename
    if copy_files:
        shutil.copy2(file_path, new_file_path)  # Copy file with metadata
    else:
        os.rename(file_path, new_file_path)


# Function to create output directory if needed
def ensure_output_directory(base_directory: str):
    """ Ensures an output dir exists for renamed files """
    output_directory = os.path.join(base_directory, "Renamed Music")
    os.makedirs(output_directory, exist_ok=True)  # Create if it doesn't exist
    return output_directory


# Define the main function for this script
def main():
    parser = argparse.ArgumentParser(description="Rename music files using metadata.")
    parser.add_argument("directory", help="Directory containing music files.")
    parser.add_argument("--copy", action="store_true", help="Copy renamed files to a new directory instead of renaming in place.")

    args = parser.parse_args()
    music_folder = args.directory.strip()
    copy_files = args.copy  # Boolean flag

    if not os.path.isdir(music_folder):
        print("Invalid directory. Please enter a valid folder path.")
        return

    # Only create "Renamed Music" directory if --copy flag is used
    output_directory = ensure_output_directory(music_folder) if copy_files else music_folder

    music_files = gather_all_music_files(music_folder)  # Gather all music files

    if not music_files:
        print("No music files found in the specified directory.")
        return

    # Process files with a progress bar
    for file in tqdm(music_files, desc="Renaming Music Files", unit="file"):
        metadata = extract_metadata_from_file(file)  # Extract metadata
        if metadata:
            file_extension = os.path.splitext(file)[1]  # Preserve file extension
            new_track_name = format_filename(metadata, file_extension)
            rename_music_files(file, new_track_name, output_directory, copy_files)


if __name__ == "__main__":
    main()