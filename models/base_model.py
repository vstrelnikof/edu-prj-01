from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Базова модель з універсальною валідацією."""

    @abstractmethod
    def validate(self):
        """Метод для перевірки даних моделі."""
        pass

    def __post_init__(self):
        self.validate()
