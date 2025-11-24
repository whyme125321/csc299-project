import click
from .storage import load

@click.group()
def chat_cmd():
    """Chat Interface"""
    pass

@chat_cmd.command()
def start():
    """Start an interactive chat session."""
    click.echo("Entering Chat Mode. Type '/exit' to quit.")
    click.echo("You can type:")
    click.echo("  /tasks  - to view your tasks")
    click.echo("  /notes  - to view your PKMS notes")
    click.echo("  /exit   - to leave chat")
    click.echo("")

    while True:
        user_input = input("You: ").strip()

        if user_input == "/exit":
            click.echo("Exiting chat.")
            break

        elif user_input == "/tasks":
            _show_tasks()

        elif user_input == "/notes":
            _show_notes()

        else:
            click.echo(f"Chatbot: You said '{user_input}'")

def _show_tasks():
    data = load("tasks.json")
    tasks = data.get("tasks", [])

    if not tasks:
        click.echo("No tasks found.")
        return

    click.echo("Your tasks:")
    for i, t in enumerate(tasks):
        status = "✔️" if t["done"] else "❌"
        click.echo(f"{i}. {t['text']} [{status}]")

def _show_notes():
    data = load("pkms.json")
    notes = data.get("notes", [])

    if not notes:
        click.echo("No notes found.")
        return

    click.echo("Your notes:")
    for i, note in enumerate(notes):
        click.echo(f"{i}. {note['title']}")
