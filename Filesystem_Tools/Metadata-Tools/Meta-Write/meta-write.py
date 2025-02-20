"""
Metadata Writer (Filename to Metadata)
---------------------------------------
Author: yung-megafone
Date: 2025-02-19
License: MIT License

Description:
This script extracts metadata from structured filenames and writes it into the actual music file's metadata.  
It ensures track number, artist, title, and featured artists are correctly embedded.

Features:
- Supports MP3, FLAC, and WAV file formats.
- Parses various filename structures intelligently.
- Recognizes multiple separators (`-`, `_`, `ft.`, `feat.`).
- Handles missing track numbers and normalizes metadata.
- Writes metadata using Mutagen.
- Includes a progress bar for large music libraries.

Usage:
    python metadata-writer.py <directory>

Example:
    python metadata-writer.py "C:\\Users\\YourName\\Music"
"""
import os
import re
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.wave import WAVE
from tqdm import tqdm

# Define flexible regex patterns
FILENAME_PATTERNS = [
    re.compile(r"(\d{1,2})\s*[-_]\s*(.*?)\s*[-_]\s*(.*?)\s*\(?feat\.?\s*(.*?)\)?(\.\w+)$", re.IGNORECASE),
    re.compile(r"(\d{1,2})\s*[-_]\s*(.*?)\s*[-_]\s*(.*?)(\.\w+)$", re.IGNORECASE),
    re.compile(r"(.*?)\s*[-_]\s*(.*?)\s*\(?feat\.?\s*(.*?)\)?(\.\w+)$", re.IGNORECASE),
    re.compile(r"(.*?)\s*[-_]\s*(.*?)(\.\w+)$", re.IGNORECASE)
]

# Alternative feature artist identifiers
FEATURED_PATTERNS = [r"feat\.?", r"ft\.?", r"featuring"]

def parse_filename(filename):
    """ Extract metadata from filename using flexible patterns. """
    for pattern in FILENAME_PATTERNS:
        match = pattern.match(filename)
        if match:
            groups = match.groups()
            metadata = {
                "track_number": groups[0] if groups[0].isdigit() else "00",
                "artist": groups[1].strip(),
                "title": groups[2].strip(),
                "featured_artists": groups[3].strip() if len(groups) > 3 and groups[3] else "",
                "extension": groups[-1]
            }
            return metadata
    
    # Fallback: Try to split the filename and extract possible metadata
    parts = re.split(r"[-_]", filename.replace(".mp3", "").replace(".flac", "").replace(".wav", ""))
    parts = [p.strip() for p in parts if p.strip()]

    # Assume first part is artist, last is title
    if len(parts) >= 2:
        metadata = {
            "track_number": "00",
            "artist": parts[0],
            "title": parts[1],
            "featured_artists": "",
            "extension": ".mp3"
        }
        
        # Check for featured artists
        for feat_pattern in FEATURED_PATTERNS:
            if re.search(feat_pattern, " ".join(parts), re.IGNORECASE):
                metadata["featured_artists"] = re.split(feat_pattern, " ".join(parts), flags=re.IGNORECASE)[-1].strip()
        
        return metadata

    return None  # Unable to extract valid metadata

def write_metadata(file_path, metadata):
    """ Writes metadata to a file using Mutagen. """
    try:
        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext == ".mp3":
            audio = EasyID3(file_path)
        elif file_ext == ".flac":
            audio = FLAC(file_path)
        elif file_ext == ".wav":
            audio = WAVE(file_path)
        else:
            print(f"Skipping unsupported file: {file_path}")
            return

        # Set metadata
        audio["tracknumber"] = metadata["track_number"]
        audio["artist"] = metadata["artist"]
        audio["title"] = metadata["title"]
        
        if metadata["featured_artists"]:
            audio["title"] += f" (feat. {metadata['featured_artists']})"

        # Save changes
        audio.save()
        tqdm.write(f"✔ Metadata applied to: {os.path.basename(file_path)}")

    except Exception as e:
        tqdm.write(f"⚠ Error writing metadata to {os.path.basename(file_path)}: {e}")

def process_files_in_directory(directory):
    """ Processes all audio files in a directory and updates their metadata. """
    supported_extensions = (".mp3", ".flac", ".wav")
    files = [f for f in os.listdir(directory) if f.lower().endswith(supported_extensions)]

    if not files:
        print("No supported music files found.")
        return

    for file in tqdm(files, desc="Processing Music Files", unit="file"):
        metadata = parse_filename(file)
        if metadata:
            file_path = os.path.join(directory, file)
            write_metadata(file_path, metadata)
        else:
            tqdm.write(f"⚠ Skipping {file} (Invalid format)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract metadata from filenames and embed it into music files.")
    parser.add_argument("directory", help="Directory containing music files.")
    args = parser.parse_args()

    if os.path.isdir(args.directory):
        process_files_in_directory(args.directory)
    else:
        print("Invalid directory. Please enter a valid path.")