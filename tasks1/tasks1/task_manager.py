import json
import os

DATA_FILE = "tasks.json"

# Load existing tasks from JSON
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save tasks to JSON
def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# Add a new task
def add_task(description):
    tasks = load_tasks()
    tasks.append({"description": description})
    save_tasks(tasks)
    print(f"✅ Task added: {description}")

# List all tasks
def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
    else:
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task['description']}")

# Search tasks by keyword
def search_tasks(keyword):
    tasks = load_tasks()
    matches = [t for t in tasks if keyword.lower() in t['description'].lower()]
    if not matches:
        print("No matching tasks.")
    else:
        print("Matching tasks:")
        for task in matches:
            print(f"- {task['description']}")

# Command-line loop
def main():
    while True:
        print("\nCommands: add, list, search, exit")
        cmd = input("> ").strip().lower()

        if cmd == "add":
            desc = input("Enter task: ")
            add_task(desc)
        elif cmd == "list":
            list_tasks()
        elif cmd == "search":
            kw = input("Enter keyword: ")
            search_tasks(kw)
        elif cmd == "exit":
            print("Goodbye!")
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

# python3 task_manager.py to run the program