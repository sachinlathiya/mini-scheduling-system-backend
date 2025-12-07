import json
import threading
from pathlib import Path
from typing import Any


class JsonStorage:
    """Thread-safe JSON file wrapper with naive locking."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def read(self) -> Any:
        with self._lock:
            if not self.path.exists():
                return []
            with self.path.open("r", encoding="utf-8") as f:
                return json.load(f)

    def write(self, data: Any) -> None:
        with self._lock:
            tmp_path = self.path.with_suffix(".tmp")
            with tmp_path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            tmp_path.replace(self.path)


