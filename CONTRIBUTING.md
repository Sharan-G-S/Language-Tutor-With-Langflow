# Contributing to Language Tutor With Langflow

Thank you for your interest in contributing to the Language Tutor project! We welcome contributions from the community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Adding New Languages](#adding-new-languages)
- [Custom Components](#custom-components)

---

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful and constructive in all interactions.

**Expected Behavior:**
- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community

---

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9 or later
- Git
- An OpenAI API key (for testing)

### Setting Up Development Environment

1. **Fork and clone the repository:**

```bash
git clone https://github.com/YOUR_USERNAME/Language-Tutor-With-Langflow.git
cd Language-Tutor-With-Langflow
```

2. **Run the development setup:**

```bash
make dev-setup
```

This command will:
- Create your `.env` file
- Install Python dependencies
- Start Docker containers
- Seed the database

3. **Configure your OpenAI API key:**

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-...
```

---

## Development Workflow

### Branch Strategy

- `main` - Stable, production-ready code
- `develop` - Integration branch for new features
- `feature/*` - New features or enhancements
- `bugfix/*` - Bug fixes
- `hotfix/*` - Critical production fixes

### Working on a Feature

1. **Create a feature branch:**

```bash
git checkout -b feature/add-french-support
```

2. **Make your changes** following our coding standards

3. **Test your changes:**

```bash
make test
make health
```

4. **Commit your changes:**

```bash
git add .
git commit -m "feat: add French language support"
```

5. **Push to your fork:**

```bash
git push origin feature/add-french-support
```

6. **Create a pull request** on GitHub

---

## Coding Standards

### Python Code Style

We follow [PEP 8](https://pep8.org/) style guidelines. Use the following tools:

- **Black** for code formatting: `black components/ scripts/ tests/`
- **flake8** for linting: `flake8 components/ scripts/ tests/`
- **isort** for import sorting: `isort components/ scripts/ tests/`

### Documentation

- Add docstrings to all functions, classes, and modules
- Use clear, descriptive variable and function names
- Include comments for complex logic
- Update README.md if you change functionality

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions or changes
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks

**Examples:**
```
feat: add German vocabulary dataset
fix: resolve database connection timeout
docs: update installation instructions
test: add tests for VocabularyLoader component
```

---

## Testing

### Running Tests

Run all tests:
```bash
make test
```

Run specific test files:
```bash
pytest tests/test_vocabulary_loader.py -v
```

Run with coverage:
```bash
pytest --cov=components tests/
```

### Writing Tests

- Place test files in the `tests/` directory
- Name test files `test_*.py`
- Use descriptive test function names: `test_load_vocabulary_success`
- Include both positive and negative test cases
- Mock external dependencies (database, APIs)

**Example test structure:**
```python
def test_component_success(mock_dependency):
    """Test successful execution."""
    # Setup
    component = MyComponent()
    
    # Execute
    result = component.method()
    
    # Assert
    assert "expected" in result.text
```

---

## Submitting Changes

### Pull Request Process

1. **Update documentation** if your changes affect usage
2. **Add tests** for new functionality
3. **Ensure all tests pass** locally
4. **Update the README** if necessary
5. **Create a pull request** with a clear description

### Pull Request Template

When creating a PR, include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No new warnings
```

### Review Process

- At least one maintainer must review and approve
- CI/CD pipeline must pass
- All comments must be addressed
- Changes may be requested before merging

---

## Adding New Languages

To add support for a new language:

### 1. Create a Vocabulary Dataset

Create a CSV file in `db/` directory (e.g., `vocab_french.csv`):

```csv
word,language,meaning,example_sentence
bonjour,French,hello,"Bonjour, comment allez-vous?"
merci,French,thank you,"Merci beaucoup pour votre aide."
ami,French,friend,"Mon ami habite à Paris."
```

### 2. Create a Seeding Script

Create a script in `scripts/` (e.g., `seed_french.py`):

```python
"""Seed French vocabulary into the database."""
import os
from seed_db import seed_vocabulary

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "db", "vocab_french.csv")
    seed_vocabulary(csv_path)
```

### 3. Update seed_all.py

Add your language to the `seed_all.py` script:

```python
languages = [
    ("Spanish", "vocab_seed.csv"),
    ("French", "vocab_french.csv"),
    ("German", "vocab_german.csv"),
    ("Tamil", "vocab_tamil.csv"),
    ("YourLanguage", "vocab_yourlanguage.csv"),  # Add here
]
```

### 3. Update Documentation

Add instructions to the README.md for using the new language:

```markdown
### Your Language Support

To use YourLanguage vocabulary:

1. Seed the database:
   ```bash
   python scripts/seed_yourlanguage.py
   ```

2. Update the Language Filter in Langflow components to "YourLanguage"
```

### 4. Submit a Pull Request

Include:
- The vocabulary CSV
- The seeding script
- Updated documentation
- At least 20 vocabulary words

---

## Custom Components

### Creating a New Component

1. **Create component file** in `components/`:

```python
from langflow.custom import Component
from langflow.io import MessageTextInput, Output
from langflow.schema.message import Message

class MyComponent(Component):
    display_name = "My Component"
    description = "Description of what it does"
    icon = "icon-name"
    name = "MyComponent"
    
    inputs = [
        MessageTextInput(
            name="input_param",
            display_name="Input Parameter",
            info="Description of input",
        ),
    ]
    
    outputs = [
        Output(
            display_name="Output",
            name="output",
            method="execute"
        ),
    ]
    
    def execute(self) -> Message:
        """Execute the component logic."""
        # Implementation
        return Message(text="Result")
```

2. **Add tests** in `tests/test_my_component.py`

3. **Update flow JSON** to include the new component

4. **Document** in README.md

---

## Questions?

If you have questions or need help:

1. Check existing [Issues](https://github.com/Sharan-G-S/Language-Tutor-With-Langflow/issues)
2. Create a new issue with the `question` label
3. Join discussions in existing pull requests

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

