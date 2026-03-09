# Language Tutor With Langflow

A stateful AI language tutor built with [Langflow](https://www.langflow.org/) and PostgreSQL. Generates personalized reading passages based on stored vocabulary with support for Spanish, French, German, and Tamil.

# Sharan G S

## Features

- 🗣️ **Multi-language support** - 110 vocabulary words across 4 languages
- 📚 **Vocabulary management** - Store and retrieve words from PostgreSQL
- ✍️ **Personalized content** - AI generates stories using your vocabulary
- 🎨 **Visual workflow** - No-code interface with Langflow
- 🧪 **Fully tested** - Comprehensive test suite with CI/CD

## Quick Start

**Prerequisites:** Docker, Docker Compose, Python 3.9+, OpenAI API key

```bash
# Clone and setup
git clone https://github.com/Sharan-G-S/Language-Tutor-With-Langflow.git
cd Language-Tutor-With-Langflow
make dev-setup

# Add your OpenAI API key to .env
echo "OPENAI_API_KEY=sk-..." >> .env

# Start services
make start
```

Visit **http://localhost:7860**, import `flows/language_tutor_flow.json`, add your API key to the OpenAI component, and start chatting!


## Makefile Commands

```bash
make dev-setup  # Complete one-command setup
make start      # Start services
make stop       # Stop services  
make restart    # Restart services
make logs       # View service logs
make health     # Check system health
make test       # Run test suite
make seed       # Seed Spanish vocabulary
make clean      # Stop and remove volumes
```

Run `make help` for all available commands.

---

## Supported Languages

| Language | Words | Seed Script |
|----------|-------|-------------|
| Spanish  | 20    | `python scripts/seed_db.py` or `make seed` |
| French   | 25    | `python scripts/seed_french.py` |
| German   | 25    | `python scripts/seed_german.py` |
| Tamil    | 40    | `python scripts/seed_tamil.py` |
| **Total** | **110** | `python scripts/seed_all.py` |

---


## Usage

### Example Conversations

**Retrieve vocabulary and generate content:**

```
User: Show me my vocabulary
Agent: You know these Spanish words: [casa, perro, gato...]

User: Write a short story using 5 of my words
Agent: [Generates a story with vocabulary]
```

**Add new words:**

```
User: Add the word "biblioteca" which means "library" in Spanish
Agent: ✓ Added "biblioteca"
```

**Switch languages:** Change `language_filter` in the Vocabulary Loader component to "French", "German", or "Tamil".

---


## Custom Components

### VocabularyLoader

Retrieves vocabulary from PostgreSQL for a given language.

**Key Inputs:** `language_filter` (Spanish, French, German, Tamil), database connection params  
**Output:** Formatted list of words with meanings

### WordAdder

Adds or updates vocabulary words in PostgreSQL.

**Key Inputs:** `word`, `language`, `meaning`, `example_sentence`, database connection params  
**Output:** Success or error message

Both components are in `components/` and connect to the `langflow-postgres` database.

---


## Project Structure

```
.
├── components/           # Custom Langflow components
│   ├── VocabularyLoader.py
│   └── WordAdder.py
├── db/                   # Database initialization
│   ├── init.sql
│   └── vocab_*.csv       # Vocabulary datasets
├── flows/                # Langflow workflow definitions
│   └── language_tutor_flow.json
├── scripts/              # Seeding and utility scripts
│   ├── seed_*.py
│   └── health_check.py
├── tests/                # Test suite
├── docker-compose.yml    # Container orchestration
└── Makefile             # Developer commands
```

---

## Development

### Testing

```bash
# Run tests
make test

# With coverage
pytest --cov=components tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and add tests
4. Run `make test` and formatters (black, flake8)
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### CI/CD

GitHub Actions runs on every push:
- Linting (black, flake8, isort)
- Tests with coverage
- Security scanning (bandit, safety)

---


## Troubleshooting

**Services won't start:**
```bash
make clean && make start
```

**Database connection errors:**
- Check containers: `docker ps | grep postgres`
- Verify credentials in `.env` match `docker-compose.yml`
- View logs: `make logs-postgres`

**Langflow can't connect to database:**
- Ensure `POSTGRES_HOST=langflow-postgres` in `.env`
- Containers must be on same network: `docker network ls`

**"No vocabulary found" error:**
```bash
make seed  # or python scripts/seed_all.py
```

**Custom components not appearing:**
- Verify `components/` directory is mounted in `docker-compose.yml`
- Restart: `make restart`

**OpenAI API errors:**
- Validate API key and credits
- Check model name (default: `gpt-4o-mini`)

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with ❤️ from Sharan G S**
