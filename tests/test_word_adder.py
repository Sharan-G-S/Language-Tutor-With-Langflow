"""
Tests for WordAdder Component
------------------------------
Tests the WordAdder custom Langflow component.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from components.WordAdder import WordAdder


@pytest.fixture
def word_adder():
    """Create a WordAdder instance with test configuration."""
    adder = WordAdder()
    adder.db_host = "localhost"
    adder.db_port = "5432"
    adder.db_name = "test_db"
    adder.db_user = "test_user"
    adder.db_password = "test_password"
    adder.language = "Spanish"
    return adder


@patch('components.WordAdder.psycopg2.connect')
def test_add_word_success(mock_connect, word_adder):
    """Test successfully adding a new word."""
    # Setup
    word_adder.word = "casa"
    word_adder.meaning = "house"
    word_adder.example_sentence = "La casa es grande."
    
    # Mock database connection
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)  # Return ID
    
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    
    # Execute
    result = word_adder.add_word()
    
    # Assertions
    assert "Successfully added" in result.text
    assert "casa" in result.text
    assert "house" in result.text
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch('components.WordAdder.psycopg2.connect')
def test_add_word_without_example(mock_connect, word_adder):
    """Test adding a word without an example sentence."""
    # Setup
    word_adder.word = "perro"
    word_adder.meaning = "dog"
    word_adder.example_sentence = ""
    
    # Mock database connection
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (2,)
    
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    
    # Execute
    result = word_adder.add_word()
    
    # Verify None is passed for example_sentence
    call_args = mock_cursor.execute.call_args[0][1]
    assert call_args[3] is None  # example_sentence should be None


def test_add_word_missing_word(word_adder):
    """Test error handling when word is not provided."""
    word_adder.word = ""
    word_adder.meaning = "something"
    
    result = word_adder.add_word()
    
    assert "Error" in result.text
    assert "No word provided" in result.text


def test_add_word_missing_meaning(word_adder):
    """Test error handling when meaning is not provided."""
    word_adder.word = "test"
    word_adder.meaning = ""
    
    result = word_adder.add_word()
    
    assert "Error" in result.text
    assert "No meaning provided" in result.text


@patch('components.WordAdder.psycopg2.connect')
def test_add_word_database_error(mock_connect, word_adder):
    """Test handling of database errors."""
    # Setup
    word_adder.word = "error"
    word_adder.meaning = "error meaning"
    
    # Mock database error
    mock_connect.side_effect = Exception("Database connection failed")
    
    # Execute
    result = word_adder.add_word()
    
    # Assertions
    assert "Error adding word" in result.text


@patch('components.WordAdder.psycopg2.connect')
def test_add_word_strips_whitespace(mock_connect, word_adder):
    """Test that word and meaning are stripped of whitespace."""
    # Setup with extra whitespace
    word_adder.word = "  hola  "
    word_adder.meaning = "  hello  "
    word_adder.example_sentence = "  example  "
    
    # Mock database connection
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    
    # Execute
    result = word_adder.add_word()
    
    # Verify stripped values were used
    call_args = mock_cursor.execute.call_args[0][1]
    assert call_args[0] == "hola"  # word (also lowercased)
    assert call_args[2] == "hello"  # meaning
    assert call_args[3] == "example"  # example_sentence


@patch('components.WordAdder.psycopg2.connect')
def test_add_word_converts_to_lowercase(mock_connect, word_adder):
    """Test that words are converted to lowercase."""
    # Setup with uppercase word
    word_adder.word = "CASA"
    word_adder.meaning = "house"
    
    # Mock database connection
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = (1,)
    
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    
    # Execute
    result = word_adder.add_word()
    
    # Verify lowercase was used
    call_args = mock_cursor.execute.call_args[0][1]
    assert call_args[0] == "casa"


def test_word_adder_inputs():
    """Test that WordAdder has required inputs."""
    adder = WordAdder()
    input_names = [inp.name for inp in adder.inputs]
    
    assert "db_host" in input_names
    assert "db_port" in input_names
    assert "db_name" in input_names
    assert "db_user" in input_names
    assert "db_password" in input_names
    assert "word" in input_names
    assert "language" in input_names
    assert "meaning" in input_names
    assert "example_sentence" in input_names


def test_word_adder_outputs():
    """Test that WordAdder has required outputs."""
    adder = WordAdder()
    output_names = [out.name for out in adder.outputs]
    
    assert "add_result" in output_names

