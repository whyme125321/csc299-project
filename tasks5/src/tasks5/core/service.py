from typing import List, Optional
from datetime import datetime, timezone

from .models import Task, TaskList
from .exceptions import TaskNotFoundError


class TaskService:
    """Business logic for task operations. Storage adapter must expose save/load methods.

    The adapter interface expected:
      - load() -> dict (with keys: version, tasks list)
      - save(data: dict) -> None
    """

    def __init__(self, storage_adapter=None, storage_path: Optional[str] = None):
        self.storage = storage_adapter
        # in-memory TaskList used as domain model
        self.tasklist = TaskList(storage_path=storage_path)
        # attempt to load persisted tasks if adapter provided
        if self.storage:
            try:
                data = self.storage.load()
                tasks = data.get('tasks', [])
                for t in tasks:
                    # create Task objects preserving ids and timestamps
                    created_at = datetime.fromisoformat(t['created_at']) if t.get('created_at') else datetime.now(timezone.utc)
                    completed_at = datetime.fromisoformat(t['completed_at']) if t.get('completed_at') else None
                    task = Task(id=t['id'], description=t['description'], is_complete=t.get('is_complete', False), created_at=created_at, completed_at=completed_at)
                    self.tasklist.tasks.append(task)
                # recalc next_id
                if self.tasklist.tasks:
                    self.tasklist.next_id = max(t.id for t in self.tasklist.tasks) + 1
            except Exception:
                # ignore load errors here; higher-level code should handle
                pass

    def create_task(self, description: str) -> Task:
        task = self.tasklist.create_task(description)
        self._persist()
        return task

    def list_tasks(self) -> List[Task]:
        return self.tasklist.get_all_tasks()

    def mark_complete(self, task_id: int) -> Task:
        task = self.tasklist.find_task(task_id)
        if task.is_complete:
            return task
        task.is_complete = True
        task.completed_at = datetime.now(timezone.utc)
        self._persist()
        return task

    def delete_task(self, task_id: int) -> None:
        task = self.tasklist.find_task(task_id)
        self.tasklist.tasks = [t for t in self.tasklist.tasks if t.id != task_id]
        self._persist()

    def _persist(self):
        if not self.storage:
            return
        data = {
            'version': '1.0',
            'tasks': [
                {
                    'id': t.id,
                    'description': t.description,
                    'is_complete': t.is_complete,
                    'created_at': t.created_at.isoformat(),
                    'completed_at': t.completed_at.isoformat() if t.completed_at else None,
                }
                for t in self.tasklist.tasks
            ]
        }
        self.storage.save(data)
