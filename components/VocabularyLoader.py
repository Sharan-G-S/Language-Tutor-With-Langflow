"""
VocabularyLoader Component
--------------------------
Custom Langflow component that connects to a PostgreSQL database and
retrieves all known vocabulary words. The agent uses this tool when
a user asks for a story or reading passage.
"""

from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema.message import Message

import psycopg2


class VocabularyLoader(Component):
    display_name = "Vocabulary Loader"
    description = "Retrieves all known vocabulary words from the PostgreSQL database."
    icon = "database"
    name = "VocabularyLoader"

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
            name="language_filter",
            display_name="Language Filter",
            value="Spanish",
            info="Filter vocabulary by language. Leave empty to retrieve all languages.",
            tool_mode=True,
        ),
    ]

    outputs = [
        Output(display_name="Vocabulary List", name="vocabulary_output", method="load_vocabulary"),
    ]

    def load_vocabulary(self) -> Message:
        """Connect to PostgreSQL and retrieve all vocabulary words."""
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                port=int(self.db_port),
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
            )
            cursor = conn.cursor()

            if self.language_filter and self.language_filter.strip():
                cursor.execute(
                    "SELECT word, meaning, example_sentence FROM vocabulary WHERE language = %s ORDER BY word",
                    (self.language_filter.strip(),),
                )
            else:
                cursor.execute(
                    "SELECT word, meaning, example_sentence FROM vocabulary ORDER BY word"
                )

            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            if not rows:
                return Message(text="No vocabulary words found in the database.")

            lines = []
            for word, meaning, example in rows:
                entry = f"- {word}: {meaning}"
                if example:
                    entry += f" (Example: {example})"
                lines.append(entry)

            result = f"Known vocabulary ({len(rows)} words):\n" + "\n".join(lines)
            return Message(text=result)

        except Exception as e:
            return Message(text=f"Error loading vocabulary: {str(e)}")
