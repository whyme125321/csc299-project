import click
from .tasks import tasks_cmd
from .pkms import pkms_cmd
from .chat import chat_cmd
from .agent import agent_cmd

@click.group()
def main():
    """CSC299 Final System"""
    pass

main.add_command(tasks_cmd)
main.add_command(pkms_cmd)
main.add_command(chat_cmd)
main.add_command(agent_cmd)

if __name__ == "__main__":
    main()
