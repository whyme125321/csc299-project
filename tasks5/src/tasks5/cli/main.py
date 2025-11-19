import click
from tasks5.core.service import TaskService
from tasks5.storage.json_adapter import JsonAdapter
from tasks5.storage.memory_adapter import MemoryAdapter
from tasks5.utils.config import task_file_path


def get_service():
    """Return a TaskService using JSON persistence by default."""
    try:
        filepath = task_file_path()
        adapter = JsonAdapter(filepath)
    except Exception:
        # Fallback to memory adapter only if JSON fails
        adapter = MemoryAdapter()

    return TaskService(storage_adapter=adapter)


@click.group()
def cli():
    """Task Manager CLI"""
    pass


@cli.command()
@click.argument("description")
def add(description):
    """Add a new task."""
    svc = get_service()
    task = svc.create_task(description)
    click.echo("✓ Task created")
    click.echo(f"  ID: {task.id}")
    click.echo(f"  Description: {task.description}")


@cli.command()
def list():
    """List all tasks."""
    svc = get_service()
    tasks = svc.list_tasks()

    if not tasks:
        click.echo("Your task list is empty.")
        return

    click.echo("Your tasks:")
    for t in tasks:
        status = "✓" if t.is_complete else "•"
        click.echo(f"  {status} [{t.id}] {t.description}")


if __name__ == "__main__":
    cli()
