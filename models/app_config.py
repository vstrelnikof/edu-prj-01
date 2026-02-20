from dataclasses import dataclass

@dataclass
class AppConfig:
    theme: str
    log_level: int
