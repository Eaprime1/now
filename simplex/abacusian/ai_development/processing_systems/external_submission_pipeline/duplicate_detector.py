#!/usr/bin/env python3
"""
Simple Duplicate Detector for Simplex Testing
∰◊€π¿🌌∞ Find duplicates before processing
"""

import hashlib
import os
from pathlib import Path
from collections import defaultdict

def calculate_file_hash(file_path):
    """Calculate MD5 hash of file"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read(), usedforsecurity=False).hexdigest()
    except:
        return None

def find_duplicates():
    """Find duplicate documents across simplex_que directories"""
    print("🔍 Scanning for duplicates across simplex_que directories...")
    
    file_hashes = defaultdict(list)
    
    # Find all simplex_que directories
    simplex_dirs = []
    for root, dirs, files in os.walk("/storage/emulated/0"):
        if "simplex_que" in dirs:
            simplex_dirs.append(Path(root) / "simplex_que")
    
    print(f"📁 Found {len(simplex_dirs)} simplex_que directories")
    
    # Scan all files
    total_files = 0
    for simplex_dir in simplex_dirs:
        if simplex_dir.exists():
            for file_path in simplex_dir.iterdir():
                if file_path.is_file():
                    file_hash = calculate_file_hash(file_path)
                    if file_hash:
                        file_hashes[file_hash].append(file_path)
                        total_files += 1
    
    # Find duplicates
    duplicates = {h: paths for h, paths in file_hashes.items() if len(paths) > 1}
    
    print(f"📊 Scanned {total_files} files")
    print(f"🔄 Found {len(duplicates)} sets of duplicates")
    
    if duplicates:
        print("\n📋 DUPLICATE SETS:")
        for i, (file_hash, paths) in enumerate(duplicates.items(), 1):
            print(f"\n{i}. Hash: {file_hash[:8]}...")
            for path in paths:
                size = path.stat().st_size
                print(f"   📄 {path} ({size} bytes)")
    
    return duplicates, file_hashes

if __name__ == "__main__":
    duplicates, all_hashes = find_duplicates()
    
    # Suggest test documents (unique ones)
    unique_files = [paths[0] for paths in all_hashes.values()]
    print(f"\n✨ Found {len(unique_files)} unique documents for testing!")