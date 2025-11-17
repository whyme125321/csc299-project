from tasks5.core.models import TaskList



def test_tasklist_create_and_get_all(tmp_path):
    tl = TaskList(storage_path=str(tmp_path / 'tasks.json'))
    t = tl.create_task('Test task')
    assert t.id == 1
    all_tasks = tl.get_all_tasks()
    assert len(all_tasks) == 1
    assert all_tasks[0].description == 'Test task'
