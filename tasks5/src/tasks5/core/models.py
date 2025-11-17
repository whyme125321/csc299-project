from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

from .exceptions import InvalidDescriptionError, TaskNotFoundError


@dataclass
class Task:
    id: int
    description: str
    is_complete: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.description or not self.description.strip():
            raise InvalidDescriptionError("Description cannot be empty")
        # normalize
        self.description = self.description.strip()


class TaskList:
    def __init__(self, storage_path: Optional[str] = None):
        self.tasks: List[Task] = []
        self.storage_path = storage_path
        self.next_id = 1

    def create_task(self, description: str) -> Task:
        t = Task(id=self.next_id, description=description)
        self.tasks.append(t)
        self.next_id += 1
        return t

    def get_all_tasks(self) -> List[Task]:
        return list(self.tasks)

    def find_task(self, task_id: int) -> Task:
        for t in self.tasks:
            if t.id == task_id:
                return t
        raise TaskNotFoundError(f"Task not found: {task_id}")
