from tasks3 import save_tasks, search_tasks

def test_search_tasks(monkeypatch, capsys):
    """Test that searching prints matching task titles."""
    # Create fake data
    tasks = [
        {"title": "Study Python", "description": "Finish chapter 5", "priority": "medium", "due_date": None},
        {"title": "Do laundry", "description": "Wash clothes", "priority": "low", "due_date": None},
    ]
    save_tasks(tasks)

    # Mock user input to search for 'study'
    monkeypatch.setattr("builtins.input", lambda _: "study")

    # Run search
    search_tasks()

    # Capture printed output
    captured = capsys.readouterr()
    assert "Study Python" in captured.out
