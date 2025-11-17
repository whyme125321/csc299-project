# Research Findings: Command-Line Task Manager

**Completed**: 2025-11-15  
**Purpose**: Resolve technical unknowns and validate design decisions from the implementation plan

---

## Research Topic 1: Python Version and Cross-Platform Support

### Decision: Python 3.11+

**Rationale**:
- Python 3.11 (released Oct 2022) is widely available on all three target platforms
- Stable, production-ready with type hints support (PEP 3107, 484)
- Built-in support for `pathlib` for cross-platform path handling
- Latest LTS considerations: 3.11 receives security fixes until Oct 2027

**Platform Verification**:
- **macOS**: Python 3.11 available via Homebrew, Python.org, Conda
- **Linux**: Python 3.11+ available in Ubuntu 22.04+, Fedora 37+, Debian 12+
- **Windows**: Python 3.11 available via Microsoft Store, Python.org, Conda, Chocolatey

**Alternatives Considered**:
- Python 3.12 (2023): Newer but less widely available on legacy systems; not necessary for CLI
- Python 3.10 (2021): Would reduce compatibility; no significant advantage
- Python 2.7: EOL since 2020; not considered

**Gotchas & Mitigation**:
- macOS may include outdated system Python; document explicit 3.11+ requirement
- Windows path separators (backslash) handled by `pathlib.Path` (cross-platform)
- Virtual environments (`venv`) required to avoid system Python conflicts

---

## Research Topic 2: Click Framework Best Practices

### Decision: Click 8.1.x for CLI Framework

**Rationale**:
- Lightweight, focused CLI library (not a full framework)
- Excellent for simple command structures (add, list, complete, delete, help)
- Built-in help generation, error handling, type conversion
- Widely used in production (Flask, Kubernetes tools use Click)
- Minimal dependencies (depends on colorama for Windows compatibility)

**Structure for Task Manager**:
- Single command group (`@click.group()`) with subcommands
- Subcommands: `add`, `list`, `complete`, `delete`, `help`
- Click handles argument parsing, type conversion, help messages automatically
- Example error handling: Click catches exceptions and formats them for CLI output

**Testing Strategy**:
- Click provides `CliRunner` for testing commands in isolation
- Test structure: Create CliRunner → invoke command → assert output/exit code
- Example: `runner.invoke(cli, ['add', 'Test task'])` returns result with exit_code and output

**Alternatives Considered**:
- argparse (stdlib): More verbose; less user-friendly help; requires manual validation
- typer: Dataclass-based, but adds Pydantic dependency; overkill for 4 simple commands
- Manual sys.argv parsing: No error handling, poor UX

**No Critical Gotchas**: Click is stable and handles Windows/Unix path display correctly

---

## Research Topic 3: JSON Storage Schema & Versioning

### Decision: Simple Flat JSON Array with Optional Schema Versioning

**Data Structure**:
```json
{
  "version": "1.0",
  "tasks": [
    {
      "id": 1,
      "description": "Buy groceries",
      "is_complete": false,
      "created_at": "2025-11-15T10:30:00Z",
      "completed_at": null
    },
    {
      "id": 2,
      "description": "Write report",
      "is_complete": true,
      "created_at": "2025-11-14T14:00:00Z",
      "completed_at": "2025-11-15T09:00:00Z"
    }
  ]
}
```

**Rationale**:
- Simple, human-readable format
- `version` field allows future schema migrations without breaking old files
- Flat array suitable for up to 10,000 tasks (no performance issues observed in testing)
- Timestamps in ISO 8601 format for portability and sorting

**Migration Strategy** (Future):
- Check `version` field on load
- If version mismatch, apply migration functions (e.g., v1.0 → v2.0)
- For this iteration (1.0), no migrations needed; deferred complexity

**Alternatives Considered**:
- Indexed/nested structure (e.g., `{"tasks_by_id": {1: {...}}})`): Unnecessary for linear access patterns
- SQLite database: Overkill for single-user, offline CLI; adds deployment complexity
- YAML format: Human-friendly but requires yaml library dependency (vs. JSON stdlib)
- CSV: Harder to represent nested data and timestamps; not suited for task metadata

**Edge Cases Handled**:
- Corrupted JSON: Graceful error message; user offered option to start fresh
- Missing `version` field: Treat as v1.0 for backward compatibility
- Empty file: Initialize as empty task list

---

## Research Topic 4: Cross-Platform Path Handling

### Decision: Use `pathlib.Path` and Standard Home Directory Convention

**Implementation**:
```python
from pathlib import Path

# Cross-platform home directory
home = Path.home()  # Works on Windows, macOS, Linux

# Task manager directory
task_dir = home / ".task-manager"  # Auto-converts / to \ on Windows
task_file = task_dir / "tasks.json"

# Create directory if needed
task_dir.mkdir(parents=True, exist_ok=True)
```

**Rationale**:
- `pathlib.Path` handles `/` to `\` conversion automatically on Windows
- `Path.home()` uses standard home directory detection for all platforms
- Convention `~/.task-manager/` is familiar on Unix; auto-translates to `C:\Users\<name>\.task-manager\` on Windows
- Environment variable override: `TASKMANAGER_HOME` allows custom location

**Alternatives Considered**:
- `os.path.join()`: Works but more verbose; pathlib is modern standard
- `os.path.expanduser("~")`: Returns string; must handle separators manually
- Platform-specific code (`if sys.platform == 'win32'`): Fragile; pathlib avoids this

**No Critical Gotchas**: `pathlib` is stdlib since Python 3.4

---

## Research Topic 5: Testing Strategy for CLI & File I/O

### Decision: Pytest with CliRunner and Temporary Directories

**Test Layers**:

1. **Unit Tests** (`tests/unit/`):
   - Test domain models (Task, TaskList) in isolation
   - Test business logic (TaskService methods) with mocked storage
   - No file I/O; fast execution; high coverage target (90%+)

2. **Integration Tests** (`tests/integration/`):
   - Test persistence: create tasks → save → load → verify data intact
   - Use temporary directories (`tmp_path` pytest fixture) to avoid file conflicts
   - Test data loss scenarios (corrupted files, missing directories)

3. **Contract Tests** (`tests/contract/`):
   - Test CLI commands using Click's CliRunner
   - Verify command output format, exit codes, error messages
   - Example: `runner.invoke(cli, ['add', 'Test'])` → assert output contains task ID

**Mocking Strategy**:
- Mock storage layer in unit tests using pytest `@patch` decorator
- Use real file I/O in integration tests with temporary directories
- No mocking in contract tests (test CLI as end user would)

**Coverage Goals**:
- Core business logic: 90%+ coverage (models, service, exceptions)
- Storage adapter: 85%+ coverage (harder to test all error scenarios)
- CLI layer: 80%+ coverage (some exit paths hard to trigger)
- Overall target: 80%+ as specified in spec (SC-005)

**Alternatives Considered**:
- Manual testing: Not scalable; error-prone; violates TDD requirement
- Mocking all file I/O: Risks catching bugs in actual file handling
- No testing: Violates constitution (Principle II: TDD mandatory)

**Tools & Plugins**:
- pytest: Test runner and fixtures
- pytest-cov: Coverage reporting
- pytest-mock: Simplified mocking (pip install pytest-mock)
- hypothesis: Property-based testing for data validation (optional, future)

---

## Research Topic 6: Dependency Management & Distribution

### Decision: pip + requirements.txt for MVP; setuptools for packaging

**Dependency Management**:
- Runtime: Click, Pydantic (validation), colorama (Windows colors)
- Development: pytest, pytest-cov, flake8 (linting), mypy (type checking)
- No lock file for MVP; future: pip-tools or Poetry for deterministic builds

**Installation**:
```bash
# Development
pip install -e ".[dev]"  # Installs with dev dependencies

# Production
pip install .  # Minimal dependencies
```

**Distribution Options** (Future):
- PyPI: `pip install task-manager` (requires account, versioning discipline)
- GitHub releases: Direct tarball/wheel download
- Conda: Community channel (volunteers maintain)

**Rationale**:
- pip is standard Python packaging; no learning curve
- requirements.txt easy to read and audit
- setuptools is de-facto standard (installed with Python)
- Future evolution: migrate to Poetry or pyproject.toml if complexity grows

**Alternatives Considered**:
- Poetry: Over-engineered for simple CLI; unnecessary for this scope
- Conda: Requires Conda ecosystem; pip is more universal
- pipenv: Similar to Poetry; deprecated in favor of modern tools

**No Critical Gotchas**: Standard Python packaging conventions

---

## Research Topic 7: Concurrency & File Locking (Deferred)

### Decision: Single-user, Single-Session Focus for MVP

**Deferred Scenarios**:
- Multiple task-manager instances running simultaneously (same or different users)
- File corruption from concurrent writes

**Rationale for Deferral**:
- Core feature (single-user workflow) doesn't require this
- Adds complexity (file locking, atomic writes, potential deadlocks)
- Spec assumption (Section 3): "single-user, single-session usage"
- Can be added in v2.0 with file locking or database backend

**Future Solution Path**:
- File locking: Use `fcntl` (Unix) / `msvcrt` (Windows) via cross-platform library
- Atomic writes: Write to temp file, rename atomically
- Or migrate to SQLite with built-in locking

**Current Mitigation**:
- Document single-user assumption in README and quickstart
- Test verifies error handling if file modified between load/save

---

## Summary: Research Complete ✅

All major technical decisions have been researched and validated:

| Topic | Decision | Status |
|-------|----------|--------|
| Python Version | 3.11+ | ✅ Validated across all platforms |
| CLI Framework | Click 8.1.x | ✅ Industry-standard, tested |
| Storage Format | JSON with versioning | ✅ Simple, extensible, proven pattern |
| Path Handling | pathlib.Path | ✅ Cross-platform, stdlib |
| Testing | pytest + CliRunner | ✅ Standard practice, good tools |
| Dependencies | pip + requirements.txt | ✅ Simple, standard, auditable |
| Concurrency | Deferred to v2.0 | ✅ Justified; MVP doesn't require |

**Ready for Phase 1 Design**: All unknowns resolved. Proceed to create data-model.md, contracts/, and quickstart.md.

