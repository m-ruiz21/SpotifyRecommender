from typing import Generic, TypeVar
from Models.Result import Result
from tekore._client import Spotify

T = TypeVar('T')
class ISpotifyTask(Generic[T]):
    """
    Interface for a task that can be run with the Spotify Client Wrapper. 
    """
    def run(self, client: Spotify) -> Result[T, str]:
        pass