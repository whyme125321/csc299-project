# Tasks1 – JSON Task Manager Prototype
### CSC 299 — AI Coding Assistants Project

## Overview
Tasks1 is the first step in building your AI-Coding Assistant System.
This milestone introduces a simple command-line task manager that stores tasks in a local JSON file.
It establishes the foundation for later features like PKMS integration, AI agents, and pytest testing.

## Features
- Add new tasks from a command-line prompt
- List all tasks after each update
- Automatic JSON persistence (loads and saves tasks to tasks.json)
- Creates storage file automatically if missing
- Simple, clean Python structure for easy extension

## How It Works
1. Loads existing tasks from tasks.json
2. Prompts the user to enter a task description
3. Appends the task to the JSON list
4. Saves updated tasks back to the file
5. Prints the full numbered task list

### How to Run
1. Navigate into the directory:
2. cd tasks1
3. Run the script:
4. python3 task_manager.py

Enter a new task: Update PKMS notes
Task added!

Current Tasks:
1. Finish CSC299 homework
2. Update PKMS notes


### Why This Matters
Tasks1 provides the basic structure your entire project builds on:
- Persistent data storage
- Command-line task interaction
- Simple architecture that expands in Tasks2 and Tasks3
- Prepares for AI-driven features later (Tasks4–Final Project)



### Example tasks.json
```json
[
    "Finish CSC299 homework",
    "Study Real Estate Unit 3"
]
