import logging
import yaml
from pathlib import Path
from models.app_config import AppConfig

class ConfigProvider:
    """Провайдер конфігурації застосунку через файл"""

    @staticmethod
    def load() -> (AppConfig | None):
        """Фабричний метод який читає конфігурацію із файлу та ініціалізує @AppConfig"""
        config_path = Path("config.yaml")
        if not config_path.exists():
            return None
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            try:
                return AppConfig(
                    theme=str(config['app']['tui']['theme']),
                    log_level=int(config['app']['log_level'])
                )
            except Exception as e:
                logging.error("Cannot create AppConfig")
                logging.exception(e)
