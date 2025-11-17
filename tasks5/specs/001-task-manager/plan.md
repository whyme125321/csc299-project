# Implementation Plan: Command-Line Task Manager

**Branch**: `001-task-manager` | **Date**: 2025-11-15 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/001-task-manager/spec.md`

## Summary

Build a command-line task manager CLI application that allows users to create, list, mark complete, and delete tasks. Tasks persist to a local JSON file. The application prioritizes simplicity, speed, and cross-platform compatibility (macOS, Linux, Windows) while following clean architecture principles with separated CLI, business logic, and persistence layers.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: Click (CLI framework), Pydantic (data validation), Pytest (testing)  
**Storage**: Local JSON file at `~/.task-manager/tasks.json` (configurable via environment variable)  
**Testing**: pytest with pytest-cov for coverage reporting  
**Target Platform**: Cross-platform CLI (macOS, Linux, Windows)  
**Project Type**: Single Python package/module  
**Performance Goals**: All commands respond in <500ms on typical hardware (SSD, modern processor)  
**Constraints**: No external services required; offline-capable; single-user focus; <10MB memory footprint  
**Scale/Scope**: Support up to 10,000 tasks without performance degradation; 2,000-3,000 lines of code target

## Constitution Check

**Specification-First Development**: ✅ PASS  
- Feature specification fully defined with user stories, requirements, success criteria before planning

**Test-Driven Development (MANDATORY)**: ✅ PASS  
- TDD requirement documented in spec (FR-010, SC-005: 80% code coverage)
- Test structure planned with unit, integration, and contract tests

**Clear Code Documentation**: ✅ PASS  
- Docstrings and README planned for CLI module and core services
- Clean architecture ensures self-explanatory code organization

**Continuous Integration & Quality Gates**: ✅ PASS  
- GitHub workflow will enforce linting (flake8), type checking (mypy), tests before merge
- Breaking change handling: semantic versioning (MAJOR.MINOR.PATCH) as per constitution

**Simplicity & Maintainability**: ✅ PASS  
- Clean architecture with 3 layers (CLI, business logic, persistence) prevents coupling
- No unnecessary frameworks; YAGNI principle applied (minimal dependencies)
- Core logic is testable and maintainable

**Gate Result**: ✅ **PASS - All constitutional requirements satisfied**

## Project Structure

### Documentation (this feature)

```text
specs/001-task-manager/
├── plan.md              # This file (speckit.plan output)
├── spec.md              # Feature specification
├── research.md          # Phase 0: research findings (to be created)
├── data-model.md        # Phase 1: entity definitions (to be created)
├── quickstart.md        # Phase 1: getting started guide (to be created)
├── contracts/           # Phase 1: API contracts (to be created)
│   └── task-cli.md      # CLI command interface specification
├── checklists/
│   └── requirements.md  # Quality validation checklist
└── tasks.md             # Phase 2: implementation tasks (created by speckit.tasks)
```

### Source Code (repository root)

```text
src/
├── __init__.py
├── cli/
│   ├── __init__.py
│   └── main.py          # Click CLI app and command handlers
├── core/
│   ├── __init__.py
│   ├── models.py        # Task and TaskList domain models
│   ├── service.py       # TaskService with business logic (CRUD operations)
│   └── exceptions.py    # Custom domain exceptions
├── storage/
│   ├── __init__.py
│   ├── adapter.py       # AbstractStorageAdapter interface
│   ├── json_adapter.py  # JSON file storage implementation
│   └── errors.py        # Storage-specific exceptions
└── utils/
    ├── __init__.py
    └── config.py        # Configuration management (file paths, env vars)

tests/
├── __init__.py
├── unit/
│   ├── test_models.py           # Task and TaskList model tests
│   ├── test_service.py          # TaskService business logic tests
│   ├── test_json_adapter.py     # JSON storage adapter tests
│   └── test_config.py           # Configuration tests
├── integration/
│   ├── test_e2e_workflow.py     # End-to-end CLI workflows
│   └── test_persistence.py      # Persistence across app restarts
└── contract/
    └── test_cli_interface.py    # CLI command contract tests

config/
├── .flake8              # Linting configuration
├── pytest.ini           # Pytest configuration with coverage settings
├── setup.py             # Package setup (dependencies, metadata)
├── requirements.txt     # Runtime dependencies
├── requirements-dev.txt # Development dependencies (pytest, flake8, mypy, etc.)
└── MANIFEST.in          # Package manifest for data files

docs/
├── README.md            # Project overview and quick start
├── ARCHITECTURE.md      # Clean architecture explanation
├── DEVELOPMENT.md       # Development guide
└── API.md               # CLI API reference

.github/workflows/
└── test.yml             # CI/CD: linting, type checking, tests on push

.gitignore
VERSION                 # Version file (1.0.0-alpha.1 initially)
```

**Structure Decision**: Single-package Python project with clean architecture layers:
1. **CLI Layer** (`src/cli/`): Handles command parsing and user I/O using Click framework
2. **Core/Business Layer** (`src/core/`): Pure domain logic (Task models, TaskService with CRUD operations)
3. **Storage Layer** (`src/storage/`): Abstract adapter pattern for file I/O (JSON initially)
4. **Utilities** (`src/utils/`): Configuration, cross-platform path handling

This structure allows each layer to be independently tested, maintains separation of concerns, and makes it easy to swap storage implementations in the future.

## Complexity Tracking

No constitutional violations requiring justification. All design decisions align with simplicity and maintainability principles.

---

## Phase 0: Research (To Be Completed)

Research tasks to resolve before Phase 1 design:

- **Python versioning**: Confirm Python 3.11+ support across macOS/Linux/Windows and identify any platform-specific gotchas
- **Click framework best practices**: Command structure, error handling, testing patterns
- **JSON schema for tasks**: Versioning strategy, migration handling for schema changes
- **Cross-platform path handling**: Best practices for home directory access and file paths on all three OS
- **Testing strategy**: pytest structure for CLI testing, mocking file I/O, property-based testing for data integrity
- **Dependency management**: Virtual environments, requirements.txt maintenance, distribution options (pip, poetry, etc.)

**Output Artifact**: `research.md` with findings, decision rationale, and alternatives considered

---

## Phase 1: Design & Contracts (To Be Completed)

### Data Model (`data-model.md` to be created)

Entities identified from spec:

1. **Task Entity**
   - Fields: id (int, auto-increment), description (str, non-empty), is_complete (bool, default=False), created_at (ISO timestamp), completed_at (optional ISO timestamp)
   - Validation: description non-empty and non-whitespace, timestamps valid ISO format
   - State transitions: incomplete → complete (one-way unless "mark incomplete" feature added)

2. **TaskList Entity**
   - Fields: tasks (List[Task]), storage_path (str, file system path)
   - Operations: add_task(description), get_all_tasks(), mark_complete(id), delete_task(id), save_to_file(), load_from_file()
   - Invariants: task IDs remain stable across save/load cycles, IDs are unique and sequential

### CLI Contracts (`contracts/task-cli.md` to be created)

Command interface specification:

```
task-manager help              # Show help message
task-manager add "<description>"  # Create task, return ID and confirmation
task-manager list              # Show all tasks with ID, description, status
task-manager complete <id>     # Mark task complete, confirm with ID
task-manager delete <id>       # Delete task, confirm with ID
```

### Quickstart Guide (`quickstart.md` to be created)

Getting started guide for developers:
- Installation steps (git clone, pip install -e .)
- First run example (creating and listing tasks)
- Running tests (pytest)
- Development workflow (TDD: write test → watch fail → implement → watch pass → refactor)

**Output Artifacts**: `data-model.md`, `contracts/task-cli.md`, `quickstart.md`, agent context updated

---

## Phase 1 Complete: Ready for Phase 2

After Phase 1 design and Phase 0 research complete, the plan transitions to Phase 2 (Task Generation) which will be handled by the `/speckit.tasks` command to break down the design into concrete implementation tasks.

**Next Step**: Run `/speckit.tasks` to generate detailed implementation tasks based on this plan and the feature spec.

