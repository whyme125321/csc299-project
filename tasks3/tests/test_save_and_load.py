import json
import os
from tasks3 import save_tasks, load_tasks

def test_save_and_load(tmp_path):
    """Test saving and loading a task list works correctly."""
    test_file = tmp_path / "tasks.json"
    os.chdir(tmp_path)  # make the program use our temp folder

    tasks = [
        {"title": "Homework", "description": "CSC299 project", "priority": "high", "due_date": None}
    ]
    save_tasks(tasks)

    # Verify file was created
    assert test_file.exists()

    # Load it back
    loaded = load_tasks()
    assert len(loaded) == 1
    assert loaded[0]["title"] == "Homework"
