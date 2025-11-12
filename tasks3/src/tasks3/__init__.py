import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task():
    title = input("Task title: ").strip()
    description = input("Description: ").strip()
    priority = input("Priority (low/medium/high): ").lower()
    due_date = input("Due date (YYYY-MM-DD or leave blank): ").strip()
    task = {
        "title": title,
        "description": description,
        "priority": priority if priority else "medium",
        "due_date": due_date if due_date else None,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print("✅ Task added successfully!")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task['title']} ({task['priority']}) - Due: {task['due_date'] or 'N/A'}")

def search_tasks():
    keyword = input("Enter keyword to search: ").lower()
    tasks = load_tasks()
    results = [t for t in tasks if keyword in t['title'].lower() or keyword in t['description'].lower()]
    if not results:
        print("No matching tasks found.")
    else:
        for t in results:
            print(f"- {t['title']}: {t['description']} (Priority: {t['priority']})")

def delete_task():
    list_tasks()
    index = int(input("Enter task number to delete: ")) - 1
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        save_tasks(tasks)
        print(f"🗑️ Deleted: {removed['title']}")
    else:
        print("Invalid task number.")

def main():
    while True:
        print("\n=== Task Manager ===")
        print("1. Add task")
        print("2. List tasks")
        print("3. Search tasks")
        print("4. Delete task")
        print("5. Quit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            search_tasks()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

def run():
    """Entry point for uv run tasks3"""
    main()

