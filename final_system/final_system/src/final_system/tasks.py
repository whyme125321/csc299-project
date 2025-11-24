import click
from .storage import load, save

TASK_FILE = "tasks.json"

@click.group()
def tasks_cmd():
    """Task Manager Commands"""
    pass

@tasks_cmd.command()
@click.argument("text")
def add(text):
    """Add a new task."""
    data = load(TASK_FILE)
    tasks = data.get("tasks", [])
    tasks.append({"text": text, "done": False})
    data["tasks"] = tasks
    save(TASK_FILE, data)
    click.echo(f"Added task: {text}")

@tasks_cmd.command()
def list():
    """List all tasks."""
    data = load(TASK_FILE)
    tasks = data.get("tasks", [])

    if not tasks:
        click.echo("No tasks found.")
        return

    for i, t in enumerate(tasks):
        status = "✔️" if t["done"] else "❌"
        click.echo(f"{i}. {t['text']} [{status}]")

@tasks_cmd.command()
@click.argument("index", type=int)
def done(index):
    """Mark a task as done by index."""
    data = load(TASK_FILE)
    tasks = data.get("tasks", [])

    if index < 0 or index >= len(tasks):
        click.echo("Invalid index")
        return

    tasks[index]["done"] = True
    save(TASK_FILE, data)
    click.echo(f"Task {index} marked as done.")

@tasks_cmd.command()
@click.argument("index", type=int)
def delete(index):
    """Delete a task by index."""
    data = load(TASK_FILE)
    tasks = data.get("tasks", [])

    if index < 0 or index >= len(tasks):
        click.echo("Invalid index")
        return

    removed = tasks.pop(index)
    save(TASK_FILE, data)
    click.echo(f"Deleted task: {removed['text']}")
