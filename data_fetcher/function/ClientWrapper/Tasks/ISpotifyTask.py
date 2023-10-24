from typing import Generic, TypeVar
from Models.Result import Result
from tekore._client import Spotify
import azure.functions as func
from abc import ABC, abstractmethod

T = TypeVar('T')
class ISpotifyTask(Generic[T], ABC):
    """
    Interface for a task that can be run with the Spotify Client Wrapper. 
    """

    def __init__(self, request: func.HttpRequest):
        self.request = request

    @abstractmethod
    def run(self, client: Spotify) -> Result[T, str]:
        """
        Runs the task with the given client.
        """
        pass

    @classmethod
    def create_task(cls, request: func.HttpRequest):
        """
        Creates a task with the given request. 
        Note:
            Created to ensure uniformity in Task creation.
        """

        return cls(request)