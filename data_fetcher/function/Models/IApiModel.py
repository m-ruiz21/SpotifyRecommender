from abc import ABC, abstractmethod

class IApiModel(ABC):
    """
    Interface for all models returned by the API
    """    

    @abstractmethod
    def to_json(self) -> str:
        pass