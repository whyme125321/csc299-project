from typing import Protocol, Dict, Any


class StorageAdapter(Protocol):
    def load(self) -> Dict[str, Any]:
        ...

    def save(self, data: Dict[str, Any]) -> None:
        ...
