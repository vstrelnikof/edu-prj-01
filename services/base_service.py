from abc import abstractmethod
from decorators.log_decorator import log_action

class BaseService:
    @abstractmethod
    @log_action
    def save(self):
        pass
    
    @abstractmethod
    @log_action
    def _reload(self):
        pass