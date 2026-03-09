"""
WordAdder Component
-------------------
Custom Langflow component that inserts a new word into the PostgreSQL
vocabulary database. The agent uses this tool when a user wants to
add a new word to their vocabulary list.
"""

from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema.message import Message

import psycopg2


class WordAdder(Component):
    display_name = "Word Adder"
    description = "Adds a new word to the vocabulary database."
    icon = "plus-circle"
    name = "WordAdder"

    inputs = [
        MessageTextInput(
            name="db_host",
            display_name="Database Host",
            value="langflow-postgres",
            info="PostgreSQL host address. Use 'langflow-postgres' when running inside Docker Compose.",
        ),
        MessageTextInput(
            name="db_port",
            display_name="Database Port",
            value="5432",
        ),
        MessageTextInput(
            name="db_name",
            display_name="Database Name",
            value="langflow_db",
        ),
        MessageTextInput(
            name="db_user",
            display_name="Database User",
            value="langflow",
        ),
        MessageTextInput(
            name="db_password",
            display_name="Database Password",
            value="langflow_secret",
            info="Password for the PostgreSQL user.",
        ),
        MessageTextInput(
            name="word",
            display_name="Word",
            info="The vocabulary word to add.",
            tool_mode=True,
        ),
        MessageTextInput(
            name="language",
            display_name="Language",
            value="Spanish",
            info="The language of the word.",
            tool_mode=True,
        ),
        MessageTextInput(
            name="meaning",
            display_name="Meaning",
            info="The English meaning of the word.",
            tool_mode=True,
        ),
        MessageTextInput(
            name="example_sentence",
            display_name="Example Sentence",
            info="An example sentence using the word (optional).",
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Result", name="add_result", method="add_word"),
    ]

    def add_word(self) -> Message:
        """Insert a new word into the vocabulary table."""
        if not self.word or not self.word.strip():
            return Message(text="Error: No word provided. Please specify a word to add.")

        if not self.meaning or not self.meaning.strip():
            return Message(text="Error: No meaning provided. Please specify the meaning of the word.")

        try:
            conn = psycopg2.connect(
                host=self.db_host,
                port=int(self.db_port),
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
            )
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO vocabulary (word, language, meaning, example_sentence)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (word) DO UPDATE SET
                    meaning = EXCLUDED.meaning,
                    example_sentence = EXCLUDED.example_sentence
                RETURNING id
                """,
                (
                    self.word.strip().lower(),
                    self.language.strip() if self.language else "Spanish",
                    self.meaning.strip(),
                    self.example_sentence.strip() if self.example_sentence else None,
                ),
            )

            row = cursor.fetchone()
            conn.commit()
            cursor.close()
            conn.close()

            word_display = self.word.strip().lower()
            meaning_display = self.meaning.strip()
            result = (
                f"Successfully added '{word_display}' (meaning: {meaning_display}) "
                f"to the vocabulary database with ID {row[0]}."
            )
            return Message(text=result)

        except Exception as e:
            return Message(text=f"Error adding word: {str(e)}")
