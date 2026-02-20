from dataclasses import dataclass
from typing import final

@final
@dataclass
class AppConfig:
    theme: str
    log_level: int
