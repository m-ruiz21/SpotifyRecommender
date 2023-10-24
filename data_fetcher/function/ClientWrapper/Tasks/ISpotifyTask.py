from typing import Generic, TypeVar
from Models.Result import Result
from tekore._client import Spotify
import azure.functions as func
from abc import ABC, abstractmethod

T = TypeVar('T')
class ISpotifyTask(Generic[T], metaclass=ABC):
    """
    Interface for a task that can be run with the Spotify Client Wrapper. 
    """

    def __init__(self, request: func.HttpRequest):
        self.request = request

    @abstractmethod
    def run(self, client: Spotify) -> Result[T, str]:
        pass

    @classmethod
    def create_task(cls, request: func.HttpRequest):
        return cls(request)