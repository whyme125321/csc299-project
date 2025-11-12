# Tasks2 – Iterated Prototype  
### CSC 299 — AI Coding Assistants Project

## Overview
Tasks2 builds on the foundation created in Tasks1 by introducing a **more structured, modular, and extensible** task management system.  
This version moves beyond a simple script and begins transitioning your project toward a **real software architecture** that will support automated testing, PKMS expansion, and AI-powered features in later milestones.

The focus of Tasks2 is:
- Cleaner and more organized Python code  
- Better JSON task storage design  
- Easier extensibility for future modules (Tasks3–Tasks5)  
- Laying the groundwork for pytest and packaging in Tasks3  

---

## Features

### **1. Improved JSON Data Structure**
Compared to Tasks1 (which used a plain list), Tasks2 uses a more structured task format that is easier to expand later.

Example structure:
```json
{
    "tasks": [
        {
            "id": 1,
            "description": "Complete CSC299 reading",
            "status": "incomplete"
        }
    ]
}
```

This allows:
- Task IDs  
- Task status fields  
- Cleaner data organization  
- Better compatibility with pytest and AI agents later  

---

### **2. Modularized Python Code**
Tasks2 reorganizes your program into functions and logical components, such as:

- `load_tasks()`  
- `save_tasks()`  
- `add_task()`  
- `list_tasks()`  

This makes the system:
- Easier to test  
- Easier to maintain  
- Easier to extend for PKMS + agent features  

---

### **3. Clear Separation of Logic**
Tasks2 eliminates the “all-in-one script” pattern from Tasks1.  
Instead, the code handles:

- **I/O management** (loading + saving JSON)  
- **User interactions** (prompting for tasks)  
- **Data formatting** (task entries)  

This separation is crucial for the pytest integration in Tasks3.

---

### **4. Persistent Task Storage**
Just like Tasks1, data is saved directly to a local JSON file (`tasks.json`).  
However, Tasks2 adds:

- Better error handling  
- Safer reads/writes  
- More consistent updates  

---

## How It Works

1. Loads all tasks from `tasks.json`
2. Displays the current task list
3. Prompts the user to add a new task
4. Assigns a unique task ID
5. Stores the task in the JSON file
6. Prints the updated task list

This workflow makes Tasks2 behave more like a “real” CLI application rather than a one-off script.

---

## Example `tasks.json`

```json
{
    "tasks": [
        {
            "id": 1,
            "description": "Finish PKMS design notes",
            "status": "incomplete"
        },
        {
            "id": 2,
            "description": "Review Real Estate Unit 3",
            "status": "complete"
        }
    ]
}
```

---

## How to Run

### Run the module:
```bash
python tasks2.py
```

(Use `python3` on macOS/Linux if needed.)

---

## Example Output

```
Current Tasks:
1. Finish PKMS design notes (incomplete)
2. Review Real Estate Unit 3 (complete)

Enter a new task: Implement Tasks3 structure
Task added!

Updated Tasks:
1. Finish PKMS design notes (incomplete)
2. Review Real Estate Unit 3 (complete)
3. Implement Tasks3 structure (incomplete)
```

---

## Why This Matters

Tasks2 is an important milestone because it transforms the initial prototype into a **more maintainable and expandable system**:

- It uses a structured data format compatible with AI features.
- It organizes your code in a modular way that supports automated testing.
- It prepares your project for the package layout introduced in Tasks3.
- It moves your CSC-299 project from “toy script” to “real software.”

Tasks2 lays the essential groundwork for:
- **Tasks3:** Python packaging, pytest, uv  
- **Tasks4:** ChatGPT API integration  
- **Final Project:** Full PKMS + AI command-line assistant  

---



