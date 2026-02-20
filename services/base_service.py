from abc import abstractmethod
from decorators.log_decorator import log_action
from providers.storage_provider import StorageProvider

class BaseService:
    """Архі-клас для реалізації сервісу"""

    def __init__(self, storage_provider: StorageProvider) -> None:
        self.storage = storage_provider
        self.reload()

    @abstractmethod
    @log_action
    def save(self):
        """Абстрактний метод для реалізації збереження даних у відповідне сховище"""
        pass
    
    @abstractmethod
    @log_action
    def reload(self):
        """Абстрактний метод для реалізації завантаження даних із відповідного сховища"""
        pass