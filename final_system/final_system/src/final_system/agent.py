import click
from .storage import load
from openai import OpenAI

client = OpenAI()

@click.group()
def agent_cmd():
    """Agent Mode"""
    pass

@agent_cmd.command()
def summarize_notes():
    """Summarize all PKMS notes using AI."""
    data = load("pkms.json")
    notes = data.get("notes", [])

    if not notes:
        click.echo("No notes to summarize.")
        return

    # Combine all notes into one text block
    text = "\n\n".join([f"{n['title']}: {n['content']}" for n in notes])

    click.echo("Summarizing notes with AI...\n")

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You summarize notes clearly and concisely."},
            {"role": "user", "content": f"Summarize the following notes:\n{text}"}
        ]
    )

    summary = response.choices[0].message.content
    click.echo("\nSummary:\n")
    click.echo(summary)

@agent_cmd.command()
def summarize_tasks():
    """Summarize your current tasks using AI."""
    data = load("tasks.json")
    tasks = data.get("tasks", [])

    if not tasks:
        click.echo("No tasks to summarize.")
        return

    text = "\n".join([f"- {t['text']} (done={t['done']})" for t in tasks])

    click.echo("Summarizing tasks with AI...\n")

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "Summarize task lists simply and clearly."},
            {"role": "user", "content": f"Summarize the following tasks:\n{text}"}
        ]
    )

    summary = response.choices[0].message.content
    click.echo("\nSummary:\n")
    click.echo(summary)
