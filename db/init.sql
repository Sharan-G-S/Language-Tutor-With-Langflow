-- Initialize the vocabulary table for the Language Tutor
-- This script runs automatically on first container startup

CREATE TABLE IF NOT EXISTS vocabulary (
    id SERIAL PRIMARY KEY,
    word VARCHAR(100) NOT NULL UNIQUE,
    language VARCHAR(50) NOT NULL DEFAULT 'Spanish',
    meaning VARCHAR(255) NOT NULL,
    example_sentence TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create an index on the language column for efficient filtering
CREATE INDEX IF NOT EXISTS idx_vocabulary_language ON vocabulary(language);

-- Create an index on the word column for fast lookups
CREATE INDEX IF NOT EXISTS idx_vocabulary_word ON vocabulary(word);
