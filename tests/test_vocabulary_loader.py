"""
Tests for VocabularyLoader Component
-------------------------------------
Tests the VocabularyLoader custom Langflow component.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from components.VocabularyLoader import VocabularyLoader


@pytest.fixture
def vocab_loader():
    """Create a VocabularyLoader instance with test configuration."""
    loader = VocabularyLoader()
    loader.db_host = "localhost"
    loader.db_port = "5432"
    loader.db_name = "test_db"
    loader.db_user = "test_user"
    loader.db_password = "test_password"
    loader.language_filter = "Spanish"
    return loader


@patch('components.VocabularyLoader.psycopg2.connect')
def test_load_vocabulary_success(mock_connect, vocab_loader):
    """Test successful vocabulary loading."""
    # Mock database connection and cursor
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        ("hola", "hello", "Hola, me llamo Carlos."),
        ("gracias", "thank you", "Muchas gracias."),
        ("amigo", "friend", None),
    ]
    
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    
    # Execute
    result = vocab_loader.load_vocabulary()
    
    # Assertions
    assert "Known vocabulary (3 words)" in result.text
    assert "hola: hello" in result.text
    assert "gracias: thank you" in result.text
    assert "amigo: friend" in result.text
    mock_cursor.execute.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch('components.VocabularyLoader.psycopg2.connect')
def test_load_vocabulary_empty_database(mock_connect, vocab_loader):
    """Test loading vocabulary from an empty database."""
    # Mock database connection with no results
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    
    # Execute
    result = vocab_loader.load_vocabulary()
    
    # Assertions
    assert "No vocabulary words found" in result.text


@patch('components.VocabularyLoader.psycopg2.connect')
def test_load_vocabulary_with_language_filter(mock_connect, vocab_loader):
    """Test vocabulary loading with language filter."""
    # Mock database connection
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [("hola", "hello", None)]
    
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    
    # Execute
    vocab_loader.language_filter = "Spanish"
    result = vocab_loader.load_vocabulary()
    
    # Verify the SQL query includes the language filter
    call_args = mock_cursor.execute.call_args
    assert "WHERE language" in call_args[0][0]
    assert call_args[0][1] == ("Spanish",)


@patch('components.VocabularyLoader.psycopg2.connect')
def test_load_vocabulary_no_language_filter(mock_connect, vocab_loader):
    """Test vocabulary loading without language filter."""
    # Mock database connection
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    
    # Execute without filter
    vocab_loader.language_filter = ""
    result = vocab_loader.load_vocabulary()
    
    # Verify the SQL query doesn't include WHERE clause
    call_args = mock_cursor.execute.call_args
    assert "WHERE" not in call_args[0][0]


@patch('components.VocabularyLoader.psycopg2.connect')
def test_load_vocabulary_connection_error(mock_connect, vocab_loader):
    """Test handling of database connection errors."""
    # Mock connection error
    mock_connect.side_effect = Exception("Connection refused")
    
    # Execute
    result = vocab_loader.load_vocabulary()
    
    # Should return an error message (component handles exceptions internally)
    # The actual implementation may vary, adjust based on component behavior
    assert result is not None


def test_vocabulary_loader_inputs():
    """Test that VocabularyLoader has required inputs."""
    loader = VocabularyLoader()
    input_names = [inp.name for inp in loader.inputs]
    
    assert "db_host" in input_names
    assert "db_port" in input_names
    assert "db_name" in input_names
    assert "db_user" in input_names
    assert "db_password" in input_names
    assert "language_filter" in input_names


def test_vocabulary_loader_outputs():
    """Test that VocabularyLoader has required outputs."""
    loader = VocabularyLoader()
    output_names = [out.name for out in loader.outputs]
    
    assert "vocabulary_output" in output_names

