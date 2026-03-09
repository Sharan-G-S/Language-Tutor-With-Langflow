"""
Seed All Languages
------------------
Loads vocabulary for all supported languages (Spanish, French, German).

Usage:
    python scripts/seed_all.py
"""

import os
import sys

# Import the seed function from the main seed script
from seed_db import seed_vocabulary


def seed_all_languages():
    """Seed vocabulary for all languages."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    languages = [
        ("Spanish", "vocab_seed.csv"),
        ("French", "vocab_french.csv"),
        ("German", "vocab_german.csv"),
        ("Tamil", "vocab_tamil.csv"),
    ]
    
    total_inserted = 0
    total_skipped = 0
    
    for language, filename in languages:
        print(f"\n{'=' * 60}")
        print(f"Seeding {language} vocabulary...")
        print('=' * 60)
        
        csv_path = os.path.join(project_root, "db", filename)
        
        if not os.path.exists(csv_path):
            print(f"⚠️  Warning: {filename} not found, skipping...")
            continue
        
        seed_vocabulary(csv_path)
    
    print(f"\n{'=' * 60}")
    print("✅ All languages seeded successfully!")
    print('=' * 60)


if __name__ == "__main__":
    seed_all_languages()

