import click
from .storage import load, save

PKMS_FILE = "pkms.json"

@click.group()
def pkms_cmd():
    """PKMS Commands"""
    pass

@pkms_cmd.command()
@click.argument("title")
@click.argument("content")
def add(title, content):
    """Add a new note to the PKMS."""
    data = load(PKMS_FILE)
    notes = data.get("notes", [])

    notes.append({
        "title": title,
        "content": content
    })

    data["notes"] = notes
    save(PKMS_FILE, data)

    click.echo(f"Added note '{title}'")

@pkms_cmd.command()
def list():
    """List all PKMS notes."""
    data = load(PKMS_FILE)
    notes = data.get("notes", [])

    if not notes:
        click.echo("No notes found.")
        return

    for i, note in enumerate(notes):
        click.echo(f"{i}. {note['title']}")

@pkms_cmd.command()
@click.argument("index", type=int)
def view(index):
    """View a specific PKMS note."""
    data = load(PKMS_FILE)
    notes = data.get("notes", [])

    if index < 0 or index >= len(notes):
        click.echo("Invalid index")
        return

    note = notes[index]
    click.echo(f"Title: {note['title']}\nContent: {note['content']}")

@pkms_cmd.command()
@click.argument("index", type=int)
def delete(index):
    """Delete a PKMS note."""
    data = load(PKMS_FILE)
    notes = data.get("notes", [])

    if index < 0 or index >= len(notes):
        click.echo("Invalid index")
        return

    removed = notes.pop(index)
    save(PKMS_FILE, data)
    click.echo(f"Deleted note '{removed['title']}'")
