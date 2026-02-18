from abc import ABC, abstractmethod
from uuid import UUID, uuid4

class BaseModel(ABC):
    id: UUID = uuid4()

    """Базова модель з універсальною валідацією."""
    @abstractmethod
    def validate(self) -> dict:
        """Метод для перевірки даних моделі."""
        pass

