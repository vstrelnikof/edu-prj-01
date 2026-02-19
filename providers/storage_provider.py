import json
from pathlib import Path
from typing import Generator

class StorageProvider:
    def __init__(self, filename: str) -> None:
        self.file = Path("data") / filename
        self.file.parent.mkdir(exist_ok=True)
        if not self.file.exists():
            self.save([])

    def load(self) -> Generator:
        """Генератор для построчного читання JSON."""
        with self.file.open("r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                yield item

    def save(self, data) -> None:
        with self.file.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)