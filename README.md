# Language Tutor With Langflow

A stateful AI language tutor built with [Langflow](https://www.langflow.org/) and PostgreSQL. The agent generates personalized reading passages based on a user's stored vocabulary and supports adding new words -- all through a visual, low-code workflow.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [Custom Components](#custom-components)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

For many beginners, the biggest barrier to building AI applications is writing complex Python code from scratch. Langflow changes this by providing a visual, drag-and-drop interface for designing AI workflows that connect to standard databases.

This project demonstrates how to build a language tutor agent that:

- Retrieves a user's known vocabulary from a PostgreSQL database
- Generates reading passages and stories tailored to those words using an LLM
- Allows users to add new words to their vocabulary through natural conversation

This is an introduction to "stateful" AI -- applications that remember and work with user data -- while keeping the technical barrier low.

---

## Architecture

```
+-------------------+       +-------------------------+       +------------------+
|                   |       |                         |       |                  |
|   User (Browser)  +------>+   Langflow (Port 7860)  +------>+   PostgreSQL     |
|                   |       |                         |       |   (Port 5432)    |
|                   |<------+   - Language Tutor Agent |<------+                  |
|                   |       |   - OpenAI LLM          |       |   vocabulary     |
|                   |       |   - VocabularyLoader     |       |   table          |
|                   |       |   - WordAdder            |       |                  |
+-------------------+       +-------------------------+       +------------------+
```

**Component Descriptions:**

| Component | Role |
|---|---|
| Langflow | Visual workflow engine hosting the AI agent |
| OpenAI LLM | Language model that generates stories and processes requests |
| VocabularyLoader | Custom component that reads vocabulary from PostgreSQL |
| WordAdder | Custom component that writes new words to PostgreSQL |
| PostgreSQL | Persistent storage for the vocabulary database |

---

## Prerequisites

Before starting, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/) (version 20.10 or later)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0 or later)
- [Python 3.9+](https://www.python.org/downloads/) (for running the seed script)
- An [OpenAI API key](https://platform.openai.com/api-keys)

---

## Setup

Follow these steps in order to get the language tutor running locally.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Sharan-G-S/Language-Tutor-With-Langflow.git
cd Language-Tutor-With-Langflow
```

### Step 2: Configure Environment Variables

Copy the example environment file and add your OpenAI API key:

```bash
cp .env.example .env
```

Open `.env` in a text editor and replace `your_openai_api_key_here` with your actual OpenAI API key:

```
OPENAI_API_KEY=sk-proj-...your-key-here...
```

The PostgreSQL credentials can be left at their default values for local development.

### Step 3: Start the Services

Launch Langflow and PostgreSQL using Docker Compose:

```bash
docker compose up -d
```

**Or use the Makefile shortcut:**

```bash
make start
```

This command starts two containers:
- **langflow-app**: The Langflow application on port `7860`
- **langflow-postgres**: The PostgreSQL database on port `5432`

Wait approximately 30-60 seconds for Langflow to fully initialize. You can monitor the startup with:

```bash
docker compose logs -f langflow
# or
make logs
```

Look for a log line indicating that Langflow is ready and listening on port 7860.

### Step 4: Seed the Vocabulary Database

**For Spanish only:**

```bash
pip install psycopg2-binary
python scripts/seed_db.py
# or
make seed
```

**For all languages (Spanish, French, German):**

```bash
pip install psycopg2-binary
python scripts/seed_all.py
```

**For specific languages:**

```bash
python scripts/seed_french.py  # French only
python scripts/seed_german.py  # German only
```

You should see output similar to:

```
Seeding complete: 20 words inserted, 0 duplicates skipped.
```

### Step 5: Verify Services Health

Check that all services are running properly:

```bash
make health
```

This will verify:
- Docker containers are running
- PostgreSQL is accessible and contains vocabulary data
- Langflow is responding on port 7860

### Step 6: Import the Langflow Flow

1. Open your browser and navigate to `http://localhost:7860`
2. In the Langflow interface, click **New Flow** or **Import**
3. Select **Import from JSON** and upload the file `flows/language_tutor_flow.json`
4. Once imported, the flow will display the following components:
   - Chat Input
   - Chat Output
   - OpenAI Model
   - Language Tutor Agent
   - Vocabulary Loader
   - Word Adder

### Step 7: Configure the OpenAI API Key in Langflow

1. Click on the **OpenAI** component in the flow
2. Enter your OpenAI API key in the `openai_api_key` field
3. The default model is set to `gpt-4o-mini`. You can change this to any supported model.

### Step 8: Run the Flow

1. Click the **Play** button or open the **Chat** panel in Langflow
2. Start interacting with the language tutor

---

## Quick Start with Makefile

For a complete setup in one command:

```bash
make dev-setup
```

This will:
1. Create your `.env` file from the template
2. Install Python dependencies
3. Start Docker containers
4. Seed the database with Spanish vocabulary

**Other useful Makefile commands:**

```bash
make help      # Show all available commands
make start     # Start all services
make stop      # Stop all services
make restart   # Restart all services
make logs      # Show logs from all services
make health    # Check service health
make test      # Run tests
make clean     # Stop services and remove volumes
```

---

## Supported Languages

This project ships with vocabulary datasets for multiple languages:

| Language | Words | Seed Command |
|----------|-------|--------------|
| Spanish | 20 | `python scripts/seed_db.py` |
| French | 25 | `python scripts/seed_french.py` |
| German | 25 | `python scripts/seed_german.py` |
| Tamil | 40 | `python scripts/seed_tamil.py` |
| All | 110 | `python scripts/seed_all.py` |

To use a different language in Langflow:
1. Change the `language_filter` input in the **Vocabulary Loader** component
2. Adjust the `language` input in the **Word Adder** component

---

## Usage

Once the flow is running, you can interact with the tutor through the Langflow chat interface. Here are example interactions:

### Generating a Reading Passage

**User:**
> Create a short story using my vocabulary words.

**Agent:** The agent will first retrieve your vocabulary from the database, then generate a story in Spanish (or your selected language) using those words, followed by translations of any new words introduced.

### Adding a New Word

**User:**
> Add the word "aventura" meaning "adventure" to my vocabulary.

**Agent:** The agent will insert the word into the database and confirm the addition.

### Requesting a Specific Topic

**User:**
> Write a passage about a day at school using my known words.

**Agent:** The agent will load your vocabulary and craft a school-themed passage using the words you already know.

### Switching Languages

To work with different languages (French, German, or Tamil):

1. Update the Language Filter in the Vocabulary Loader component to "French", "German", or "Tamil"
2. Seed the respective language data using the appropriate script
3. Adjust your prompts to request content in that language

**Example for Tamil:**
```bash
python scripts/seed_tamil.py
```
Then in Langflow, set the language filter to "Tamil" and ask the agent to create stories in Tamil using your vocabulary.

---

## Custom Components

This project includes two custom Langflow components located in the `components/` directory.

### VocabularyLoader

**File:** `components/VocabularyLoader.py`

Connects to the PostgreSQL database and retrieves all vocabulary words for a given language. The component returns a formatted list of words with their meanings and example sentences.

**Inputs:**
| Input | Description | Default |
|---|---|---|
| db_host | PostgreSQL host | `langflow-postgres` |
| db_port | PostgreSQL port | `5432` |
| db_name | Database name | `langflow_db` |
| db_user | Database username | `langflow` |
| db_password | Database password | `langflow_secret` |
| language_filter | Filter by language | `Spanish` |

### WordAdder

**File:** `components/WordAdder.py`

Inserts a new vocabulary word into the PostgreSQL database. If the word already exists, it updates the meaning and example sentence.

**Inputs:**
| Input | Description | Default |
|---|---|---|
| db_host | PostgreSQL host | `langflow-postgres` |
| db_port | PostgreSQL port | `5432` |
| db_name | Database name | `langflow_db` |
| db_user | Database username | `langflow` |
| db_password | Database password | `langflow_secret` |
| word | The word to add | -- |
| language | Language of the word | `Spanish` |
| meaning | English meaning | -- |
| example_sentence | Example usage | -- |

---

## Project Structure

```
Language-Tutor-With-Langflow/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI/CD pipeline
├── components/
│   ├── VocabularyLoader.py      # Custom component: retrieves vocabulary
│   └── WordAdder.py             # Custom component: adds new words
├── db/
│   ├── init.sql                 # Database schema initialization
│   ├── vocab_seed.csv           # Spanish vocabulary (20 words)
│   ├── vocab_french.csv         # French vocabulary (25 words)
│   ├── vocab_german.csv         # German vocabulary (25 words)
│   └── vocab_tamil.csv          # Tamil vocabulary (40 words)
├── flows/
│   └── language_tutor_flow.json # Langflow flow definition for import
├── scripts/
│   ├── requirements.txt         # Python dependencies
│   ├── seed_db.py               # Database seeding script (Spanish)
│   ├── seed_french.py           # Seed French vocabulary
│   ├── seed_german.py           # Seed German vocabulary
│   ├── seed_tamil.py            # Seed Tamil vocabulary
│   ├── seed_all.py              # Seed all languages
│   └── health_check.py          # Service health check script
├── tests/
│   ├── __init__.py
│   ├── test_vocabulary_loader.py # Tests for VocabularyLoader
│   └── test_word_adder.py       # Tests for WordAdder
├── .env.example                 # Environment variable template
├── .gitignore                   # Git ignore rules
├── CONTRIBUTING.md              # Contribution guidelines
├── docker-compose.yml           # Docker Compose configuration
├── LICENSE                      # Project license (MIT)
├── Makefile                     # Convenient command shortcuts
├── pytest.ini                   # Pytest configuration
└── README.md                    # This file
```

---

## Testing

This project includes a comprehensive test suite for the custom components.

### Running Tests

Run all tests:
```bash
make test
```

Or manually:
```bash
pip install -r scripts/requirements.txt
pytest tests/ -v
```

### Test Coverage

Run tests with coverage report:
```bash
pytest --cov=components tests/
```

### Writing Tests

Tests are located in the `tests/` directory. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on writing tests.

---

## Development

### Making Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `make test`
5. Check code quality: `black components/` and `flake8 components/`
6. Commit: `git commit -m "feat: add my feature"`
7. Push and create a pull request

### Code Quality

We use automated tools for code quality:
- **Black** for code formatting
- **flake8** for linting
- **pytest** for testing
- **GitHub Actions** for CI/CD

### Contributing

We welcome contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development workflow
- Coding standards
- How to add new languages
- How to create custom components
- Pull request process

---

## Troubleshooting

### Langflow is not accessible at localhost:7860

- Ensure both containers are running: `docker compose ps`
- Check Langflow logs for errors: `docker compose logs langflow`
- Wait at least 60 seconds after starting the containers; Langflow takes time to initialize

### Database connection errors in custom components

- Verify the database host is set to `langflow-postgres` (the Docker Compose service name)
- If running the seed script locally, use `localhost` as the host
- Ensure the PostgreSQL container is healthy: `docker compose ps`

### Seed script fails to connect

- Confirm that port `5432` is exposed and not blocked by another service
- Ensure the PostgreSQL container is fully started before running the seed
- Verify credentials in `.env` match those in `docker-compose.yml`

### Custom components not appearing in Langflow

- Confirm the `components/` directory is mounted correctly in `docker-compose.yml`
- Restart the Langflow container: `docker compose restart langflow`
- Check Langflow logs for component loading errors

### OpenAI API errors

- Verify your API key is valid and has available credits
- Check that the model name is correct (default: `gpt-4o-mini`)
- Ensure your network allows outbound HTTPS connections

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
