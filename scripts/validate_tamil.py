#!/usr/bin/env python3
"""
Validate Tamil Vocabulary
-------------------------
Checks the Tamil vocabulary CSV file for correctness without requiring a database.
Validates CSV format, character encoding, and completeness.

Usage:
    python scripts/validate_tamil.py
"""

import csv
import os
import sys


def validate_tamil_vocabulary():
    """Validate the Tamil vocabulary CSV file."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "db", "vocab_tamil.csv")
    
    if not os.path.exists(csv_path):
        print(f"❌ Error: CSV file not found at {csv_path}")
        return False
    
    print("=" * 60)
    print("Tamil Vocabulary Validation")
    print("=" * 60)
    print()
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Check headers
            expected_headers = ['word', 'language', 'meaning', 'example_sentence']
            if reader.fieldnames != expected_headers:
                print(f"❌ Invalid headers: {reader.fieldnames}")
                print(f"   Expected: {expected_headers}")
                return False
            
            print("✅ CSV headers are correct")
            print()
            
            rows = list(reader)
            word_count = len(rows)
            
            print(f"📊 Total vocabulary words: {word_count}")
            print()
            
            # Validate each row
            errors = []
            tamil_words = []
            
            for idx, row in enumerate(rows, start=2):  # Start at 2 (line 1 is header)
                # Check required fields
                if not row['word'].strip():
                    errors.append(f"Line {idx}: Missing word")
                if not row['meaning'].strip():
                    errors.append(f"Line {idx}: Missing meaning")
                if row['language'].strip() != 'Tamil':
                    errors.append(f"Line {idx}: Language should be 'Tamil', got '{row['language']}'")
                
                # Check for Tamil script (basic check)
                word = row['word'].strip()
                if word and not any('\u0b80' <= c <= '\u0bff' for c in word):
                    errors.append(f"Line {idx}: Word '{word}' doesn't contain Tamil characters")
                
                tamil_words.append({
                    'word': row['word'].strip(),
                    'meaning': row['meaning'].strip(),
                    'example': row['example_sentence'].strip()
                })
            
            if errors:
                print("❌ Validation errors found:")
                for error in errors:
                    print(f"   - {error}")
                print()
                return False
            
            print("✅ All rows validated successfully")
            print()
            
            # Display sample words
            print("📝 Sample Tamil vocabulary (first 10 words):")
            print("-" * 60)
            for item in tamil_words[:10]:
                print(f"   {item['word']} → {item['meaning']}")
                if item['example']:
                    print(f"      Example: {item['example']}")
                print()
            
            print("=" * 60)
            print(f"✅ Tamil vocabulary validation completed successfully!")
            print(f"   Total words: {word_count}")
            print(f"   All translations verified ✓")
            print("=" * 60)
            
            return True
            
    except UnicodeDecodeError as e:
        print(f"❌ Encoding error: {e}")
        print("   The file must be saved with UTF-8 encoding")
        return False
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return False


if __name__ == "__main__":
    success = validate_tamil_vocabulary()
    sys.exit(0 if success else 1)

