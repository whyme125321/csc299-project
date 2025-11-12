# Tasks3 – Pytest and UV Integration
### CSC 299 — AI Coding Assistants Project

## Overview
Tasks3 evolves your project from simple scripts into a **structured, testable, and environment-managed Python package**.  
This milestone introduces three major upgrades:

1. A proper **Python package layout** using `src/`  
2. **Automated testing** with `pytest`  
3. **Environment and dependency management** using **uv**

This brings your CSC-299 project closer to professional software engineering standards and prepares it for PKMS + AI-agent integration in later tasks.

---

## Features
- **Python package structure**  
  Your code now lives inside:
  ```
  src/tasks3/
  ```

- **Automated testing with pytest**  
  A dedicated `tests/` directory lets you verify behavior with:
  ```bash
  uv run pytest
  ```

- **uv-based environment management**  
  Ensures consistent, reproducible execution across systems.

- **Full compatibility with previous tasks**  
  All task-handling logic from Tasks1/Tasks2 remains intact, just organized better.


---

## How It Works

### 1. Python Package (`src/` directory)
Your code is now importable as a package:

```python
from tasks3 import tasks3
```

This is necessary for:
- pytest imports  
- AI agents interacting with your modules later  
- Cleaner project organization  

### 2. Pytest Integration
The `tests/` folder contains automated test files like:

```
tests/test_tasks3.py
```

Running tests is now simple and environment-safe:

```bash
uv run pytest
```

This ensures:
- Code correctness  
- No regressions when adding new features  
- You are following standard software engineering practices  

### 3. uv Environment Management
Your `pyproject.toml` defines dependencies.

To run Tasks3 using uv:
```bash
cd tasks3
uv run tasks3
```

To run tests:
```bash
uv run pytest
```

uv guarantees that:
- The right Python version is used  
- Dependencies are isolated  
- Pytest runs the same way on any machine  

---

## How to Run

### Run the main module:
```bash
cd tasks3
uv run tasks3
```

### Run all tests:
```bash
uv run pytest
```

---

## Why This Matters

Tasks3 transforms your project into a professional-style Python package.  
This matters because:

- You now have **automated testing**, which is required for reliable software.  
- Your project becomes **modular**, allowing AI agents to interact with your code.  
- Using **uv** prepares you for repeatable development environments, a real-world engineering requirement.  
- Tasks3 sets the stage for Tasks4–Final Project, where you integrate ChatGPT, PKMS workflows, and a terminal-based assistant.

This milestone is the bridge between **simple prototypes** and a **full AI-backed application**.

---



