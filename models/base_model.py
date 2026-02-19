import logging
from dataclasses import dataclass
from abc import ABC, abstractmethod
from uuid import uuid4

@dataclass
class BaseModel(ABC):
    def __init__(self) -> None:
        self.id = uuid4()

    """Базова модель з універсальною валідацією."""
    @abstractmethod
    def validate(self) -> dict:
        """Метод для перевірки даних моделі."""
        pass

    def is_valid(self) -> bool:
        validation_result: dict = self.validate()
        is_failed: bool = any(result for _, result in validation_result.items()
                              if not result)
        if is_failed:
            logging.warning(f"Model validation failed: {str(validation_result)}")
        
        return not is_failed

