#!/usr/bin/env python3
import json
import os
from typing import List, Dict

DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")

def load_tasks() -> List[Dict]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks: List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def add_task() -> None:
    title = input("Task title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    details = input("Details: ").strip()
    priority = input("Priority (low/med/high) [med]: ").strip() or "med"
    tags = input("Tags (comma-separated, optional): ").strip()
    task = {
        "title": title,
        "details": details,
        "priority": priority,
        "tags": [t.strip() for t in tags.split(",")] if tags else []
    }
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print("✅ Task added.")

def list_tasks() -> None:
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for i, task in enumerate(tasks, start=1):
        tags_str = f" [{', '.join(task['tags'])}]" if task.get("tags") else ""
        print(f"{i}. {task['title']} (priority: {task.get('priority','med')}){tags_str}\n   {task.get('details','')}\n")

def search_tasks() -> None:
    term = input("Search term: ").lower().strip()
    if not term:
        print("No search term provided.")
        return
    tasks = load_tasks()
    matches = [t for t in tasks if term in t["title"].lower() or term in t["details"].lower() or term in " ".join(t.get("tags",[])).lower()]
    if not matches:
        print("No matches.")
        return
    for t in matches:
        tags_str = f" [{', '.join(t['tags'])}]" if t.get("tags") else ""
        print(f"• {t['title']} (priority: {t.get('priority','med')}){tags_str}\n  {t.get('details','')}\n")

def delete_task() -> None:
    tasks = load_tasks()
    if not tasks:
        print("No tasks to delete.")
        return
    list_tasks()
    num = input("Task number to delete (or 'c' to cancel): ").strip()
    if num.lower() == 'c':
        print("Cancelled.")
        return
    if not num.isdigit():
        print("Invalid number.")
        return
    idx = int(num) - 1
    if idx < 0 or idx >= len(tasks):
        print("Invalid number.")
        return
    removed = tasks.pop(idx)
    save_tasks(tasks)
    print(f"🗑 Deleted: {removed['title']}")

def help_text() -> None:
    print("Commands: add, list, search, delete, help, quit")

def main() -> None:
    print("tasks2 — simple task manager (type 'help' for commands)")
    while True:
        cmd = input("> ").strip().lower()
        if cmd == "add":
            add_task()
        elif cmd == "list":
            list_tasks()
        elif cmd == "search":
            search_tasks()
        elif cmd == "delete":
            delete_task()
        elif cmd == "help":
            help_text()
        elif cmd == "quit" or cmd == "exit":
            print("Goodbye!")
            break
        elif cmd == "":
            continue
        else:
            print("Unknown command. Type 'help'.")

if __name__ == "__main__":
    main()
