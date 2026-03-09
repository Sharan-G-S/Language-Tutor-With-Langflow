"""
Seed French Vocabulary
----------------------
Loads French vocabulary words from db/vocab_french.csv into the database.

Usage:
    python scripts/seed_french.py
"""

import os
import sys

# Import the seed function from the main seed script
from seed_db import seed_vocabulary


if __name__ == "__main__":
    # Resolve path relative to the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "db", "vocab_french.csv")
    
    print("Seeding French vocabulary...")
    seed_vocabulary(csv_path)

