import json
from pathlib import Path


class StorageManager:
    def __init__(self, filename: str):
        self.file = Path("data") / filename
        self.file.parent.mkdir(exist_ok=True)
        if not self.file.exists():
            self.save([])

    def load(self):
        """Генератор для построчного читання JSON."""
        with self.file.open("r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                yield item

    def save(self, data):
        with self.file.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)