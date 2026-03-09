"""
Database Seeding Script
-----------------------
Reads vocabulary words from db/vocab_seed.csv and inserts them into the
PostgreSQL vocabulary table. Duplicates are skipped automatically.

Usage:
    pip install psycopg2-binary
    python scripts/seed_db.py
"""

import csv
import os
import sys

import psycopg2


def get_connection():
    """Establish a connection to the PostgreSQL database."""
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "langflow_db"),
        user=os.getenv("POSTGRES_USER", "langflow"),
        password=os.getenv("POSTGRES_PASSWORD", "langflow_secret"),
    )


def seed_vocabulary(csv_path):
    """Read the CSV file and insert vocabulary rows into the database."""
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        sys.exit(1)

    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0
    skipped = 0

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                cursor.execute(
                    """
                    INSERT INTO vocabulary (word, language, meaning, example_sentence)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (word) DO NOTHING
                    """,
                    (
                        row["word"].strip(),
                        row["language"].strip(),
                        row["meaning"].strip(),
                        row.get("example_sentence", "").strip(),
                    ),
                )
                if cursor.rowcount > 0:
                    inserted += 1
                else:
                    skipped += 1
            except Exception as e:
                print(f"Error inserting word '{row.get('word', '?')}': {e}")
                conn.rollback()
                continue

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Seeding complete: {inserted} words inserted, {skipped} duplicates skipped.")


if __name__ == "__main__":
    # Resolve path relative to the project root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "db", "vocab_seed.csv")
    seed_vocabulary(csv_path)
