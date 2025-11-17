import json
from pathlib import Path
from typing import Dict, Any

from .adapter import StorageAdapter


class JsonAdapter:
    """JSON file storage adapter with atomic writes."""

    def __init__(self, path: Path):
        self.path = Path(path)

    def load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return {'version': '1.0', 'tasks': []}
        try:
            with self.path.open('r', encoding='utf-8') as fh:
                return json.load(fh)
        except json.JSONDecodeError:
            raise

    def save(self, data: Dict[str, Any]) -> None:
        # atomic write: write to temp file then rename
        tmp = self.path.with_suffix('.tmp')
        tmp.parent.mkdir(parents=True, exist_ok=True)
        with tmp.open('w', encoding='utf-8') as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.flush()
        tmp.replace(self.path)
import json
from pathlib import Path
from typing import Dict, Any


class JsonAdapter:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path).expanduser()
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> Dict[str, Any]:
        if not self.file_path.exists():
            return {'version': '1.0', 'tasks': []}
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise

    def save(self, data: Dict[str, Any]) -> None:
        # Atomic write: write to temp file then rename
        tmp = self.file_path.with_suffix('.tmp')
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        tmp.replace(self.file_path)
