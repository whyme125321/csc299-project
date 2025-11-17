from pathlib import Path
import os


def task_manager_home() -> Path:
    """Return the directory Path for task manager data.

    Respects TASKMANAGER_HOME environment variable if set, otherwise uses
    ~/.task-manager
    """
    env = os.environ.get('TASKMANAGER_HOME')
    if env:
        p = Path(env).expanduser()
    else:
        p = Path.home() / '.task-manager'
    return p


def task_file_path() -> Path:
    p = task_manager_home()
    p.mkdir(parents=True, exist_ok=True)
    return p / 'tasks.json'
from pathlib import Path
import os


def get_default_storage_path() -> str:
    # Allow override with environment variable
    env = os.getenv('TASKMANAGER_HOME')
    if env:
        p = Path(env).expanduser()
        p.mkdir(parents=True, exist_ok=True)
        return str((p / 'tasks.json').resolve())
    home = Path.home()
    p = home / '.task-manager'
    p.mkdir(parents=True, exist_ok=True)
    return str((p / 'tasks.json').resolve())
