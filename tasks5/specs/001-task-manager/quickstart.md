# Quickstart Guide: Command-Line Task Manager Development

**Date**: 2025-11-15  
**Audience**: Developers implementing this feature  
**Prerequisites**: Python 3.11+, git, basic CLI knowledge

---

## 1. Project Setup

### Clone Repository

```bash
cd ~/projects
git clone <repository-url>
cd task-manager
git checkout 001-task-manager  # Switch to feature branch
```

### Set Up Python Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Verify Python version
python --version  # Should show 3.11.x or higher
```

### Install Dependencies

```bash
# Install package in development mode with dev dependencies
pip install -e ".[dev]"

# Verify installation
task-manager --help
```

This installs:
- **Runtime**: Click, Pydantic, colorama
- **Development**: pytest, pytest-cov, flake8, mypy

---

## 2. Project Structure Overview

```
task-manager/
├── src/
│   ├── cli/                    # CLI layer (Click commands)
│   │   ├── __init__.py
│   │   └── main.py             # Main CLI entry point
│   ├── core/                   # Business logic layer
│   │   ├── __init__.py
│   │   ├── models.py           # Task, TaskList domain models
│   │   ├── service.py          # TaskService with CRUD operations
│   │   └── exceptions.py       # Domain exceptions
│   ├── storage/                # Persistence layer
│   │   ├── __init__.py
│   │   ├── adapter.py          # Storage adapter interface
│   │   ├── json_adapter.py     # JSON implementation
│   │   └── errors.py           # Storage exceptions
│   └── utils/
│       ├── __init__.py
│       └── config.py           # Configuration management
├── tests/
│   ├── unit/                   # Unit tests (no I/O)
│   ├── integration/            # Integration tests (real I/O)
│   └── contract/               # CLI interface tests
├── setup.py                    # Package metadata
├── requirements.txt            # Runtime dependencies
├── requirements-dev.txt        # Dev dependencies
└── pytest.ini                  # Pytest configuration
```

---

## 3. Development Workflow (TDD)

The **Test-Driven Development** workflow is mandatory per the project constitution:

### Step 1: Write a Failing Test

```bash
# Open tests/unit/test_models.py
# Add a test for creating a task with an invalid description

def test_task_creation_with_empty_description_raises_error():
    """Test that creating a task with empty description raises InvalidDescriptionError"""
    with pytest.raises(InvalidDescriptionError):
        task = Task(description="", created_at=datetime.now(timezone.utc))
```

### Step 2: Run Tests and Watch Fail (Red Phase)

```bash
pytest tests/unit/test_models.py::test_task_creation_with_empty_description_raises_error -v

# Output: FAILED (expected - the feature doesn't exist yet)
```

### Step 3: Implement the Feature (Green Phase)

```python
# In src/core/models.py
class Task:
    def __init__(self, description: str, created_at: datetime):
        if not description or not description.strip():
            raise InvalidDescriptionError("Description cannot be empty")
        self.description = description.strip()
        self.created_at = created_at
```

### Step 4: Run Tests Again (Green Phase)

```bash
pytest tests/unit/test_models.py::test_task_creation_with_empty_description_raises_error -v

# Output: PASSED ✓
```

### Step 5: Refactor for Clarity (Refactor Phase)

```python
# Improve code clarity, variable naming, remove duplication
# Run all tests to ensure nothing breaks
pytest tests/ --cov=src --cov-report=term-missing
```

### Repeat for Each Feature

1. Write test → 2. Run (FAIL) → 3. Implement → 4. Run (PASS) → 5. Refactor → Repeat

---

## 4. Running Tests

### Run All Tests

```bash
pytest

# or with verbose output
pytest -v

# or with coverage report
pytest --cov=src --cov-report=html
```

### Run Specific Test Layer

```bash
# Unit tests only (fast, no I/O)
pytest tests/unit/ -v

# Integration tests (slower, uses files)
pytest tests/integration/ -v

# CLI contract tests
pytest tests/contract/ -v
```

### Run Single Test File

```bash
pytest tests/unit/test_models.py -v
```

### Run Single Test Function

```bash
pytest tests/unit/test_models.py::test_task_creation_with_valid_description -v
```

### Watch Tests During Development

```bash
# Install pytest-watch
pip install pytest-watch

# Auto-run tests on file changes
ptw -- --cov=src
```

---

## 5. First Manual Test

### Create a Test Task

```bash
# Ensure in activated venv
source venv/bin/activate

# Create first task
task-manager add "Learn Python"

# Expected output:
# ✓ Task created
#   ID: 1
#   Description: Learn Python
```

### List Tasks

```bash
task-manager list

# Expected output:
# Your Tasks:
#   1     Learn Python
```

### Mark Complete

```bash
task-manager complete 1

# Expected output:
# ✓ Task marked complete
#   ID: 1
#   Description: Learn Python
```

### Verify Persistence

```bash
# Exit and restart the application
task-manager list

# Expected output (data persists):
# Your Tasks:
#   1  ✓  Learn Python
```

---

## 6. Code Quality

### Linting (Check Code Style)

```bash
flake8 src/ tests/

# Expected: No output (all rules satisfied)
```

### Type Checking

```bash
mypy src/

# Expected: No errors
```

### Coverage Report

```bash
pytest --cov=src --cov-report=term-missing --cov-report=html

# View HTML report
open htmlcov/index.html
```

**Target**: 80% coverage minimum (per specification SC-005)

---

## 7. Architecture Layers

### CLI Layer (src/cli/main.py)

Handles command parsing and user interaction. **Do not** put business logic here.

```python
@click.group()
def cli():
    """Task Manager CLI"""
    pass

@cli.command()
@click.argument('description')
def add(description):
    """Add a new task"""
    service = TaskService()
    task = service.create_task(description)
    click.echo(f"✓ Task created\n  ID: {task.id}\n  Description: {task.description}")
```

### Core/Business Layer (src/core/)

Contains domain models and pure business logic. **No external dependencies** (no Click, no file I/O).

```python
class TaskService:
    def __init__(self, storage_adapter):
        self.storage = storage_adapter
    
    def create_task(self, description: str) -> Task:
        """Business logic for creating a task"""
        # Validation, ID generation, timestamp setting
        task = Task(description=description, created_at=datetime.now(timezone.utc))
        self.storage.save(task)
        return task
```

### Storage Layer (src/storage/)

Handles file I/O through adapter pattern. **Easy to swap** implementations.

```python
class JsonStorageAdapter:
    def save(self, tasks: List[Task]) -> None:
        """Save tasks to JSON file"""
        # Serialize to JSON
        # Write to disk
        pass

    def load(self) -> List[Task]:
        """Load tasks from JSON file"""
        # Read from disk
        # Deserialize from JSON
        pass
```

**Benefit**: Each layer is independently testable and replaceable.

---

## 8. Common Development Tasks

### Add a New Command (e.g., "archive")

1. **Write test** in `tests/contract/test_cli_interface.py`
2. **Implement CLI** in `src/cli/main.py` (calls service)
3. **Add service method** in `src/core/service.py`
4. **Run tests** and verify

### Fix a Bug

1. **Write test** that reproduces the bug (currently failing)
2. **Fix code** to make test pass
3. **Verify** no regressions with full test suite

### Improve Code Quality

1. Run `flake8 src/`
2. Fix style issues
3. Run `mypy src/`
4. Fix type issues
5. Run `pytest` to ensure tests still pass

---

## 9. Before Committing

```bash
# 1. Run full test suite
pytest --cov=src -v

# 2. Check linting
flake8 src/ tests/

# 3. Check type hints
mypy src/

# 4. Verify coverage >= 80%
pytest --cov=src --cov-report=term-missing | grep TOTAL

# 5. Manual smoke test
task-manager help
task-manager add "Test commit"
task-manager list
task-manager delete 1

# 6. Commit with clear message
git add .
git commit -m "feat: implement add command with validation"
git push origin 001-task-manager
```

---

## 10. Useful Resources

- **Click Documentation**: https://click.palletsprojects.com/
- **Pytest Documentation**: https://docs.pytest.org/
- **Python pathlib**: https://docs.python.org/3/library/pathlib.html
- **Pydantic Validation**: https://docs.pydantic.dev/
- **Clean Architecture**: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html

---

## 11. Troubleshooting

### `command not found: task-manager`

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall package
pip install -e ".[dev]"
```

### `ModuleNotFoundError: No module named 'click'`

```bash
# Install dependencies
pip install -e ".[dev]"
```

### Tests Fail Intermittently

```bash
# Check for file permission issues
rm -rf ~/.task-manager
pytest tests/integration/ -v

# Check for timezone issues (use UTC)
# All timestamps should be in UTC
```

### Corrupted tasks.json

```bash
# Remove and regenerate
rm ~/.task-manager/tasks.json
task-manager list  # Initializes empty list
```

---

## Next Steps

1. ✅ Environment setup (you are here)
2. Start implementing core models (src/core/models.py)
3. Implement TaskService (src/core/service.py)
4. Implement JSON storage adapter (src/storage/json_adapter.py)
5. Implement CLI commands (src/cli/main.py)
6. Write and pass all tests
7. Create pull request for review

**Estimated Timeline**: 2-3 days for MVP implementation with TDD

