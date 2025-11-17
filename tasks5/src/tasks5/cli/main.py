import click

@click.group()
def cli():
    """Task Manager CLI"""
    pass


@cli.command()
@click.argument('description', nargs=1)
def add(description):
    """Add a new task (placeholder)
    """
    click.echo(f"✓ Task created\n  ID: 1\n  Description: {description}")


@cli.command()
def list():
    """List tasks (placeholder)"""
    click.echo("Your task list is empty.")


if __name__ == '__main__':
    cli()
