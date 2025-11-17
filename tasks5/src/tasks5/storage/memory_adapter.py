from typing import Dict, Any


class MemoryAdapter:
    """Simple in-memory storage adapter (non-persistent). Used during unit tests."""

    def __init__(self, initial: Dict[str, Any] = None):
        self._data = initial or {'version': '1.0', 'tasks': []}

    def load(self) -> Dict[str, Any]:
        return self._data

    def save(self, data: Dict[str, Any]) -> None:
        # shallow copy
        self._data = dict(data)
