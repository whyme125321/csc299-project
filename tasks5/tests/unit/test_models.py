import pytest
from datetime import datetime, timezone

from tasks5.core.exceptions import InvalidDescriptionError
from tasks5.core.models import Task


def test_task_creation_with_empty_description_raises_error():
    with pytest.raises(InvalidDescriptionError):
        Task(id=1, description="", created_at=datetime.now(timezone.utc))
