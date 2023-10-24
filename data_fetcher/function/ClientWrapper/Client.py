import tekore as tk
from tekore._client import Spotify
from Models.Result import Result
import os
from typing import TypeVar 
from ValidationUtils.TaskType import ISpotifyTask

T = TypeVar('T')
class SpotifyClient:
    __client: Spotify = None

    def __init__(self) -> None:
        authorize_res = self.__authorize() 
        self.__client = authorize_res.unwrap() 


    @classmethod
    def start(cls) -> Result[Spotify, str]:
        """
        Safely initializes the Spotify client without exception.

        Returns:
            Result[Spotify, str]: The Spotify client if the initialization was successful, or an error message otherwise.
        """
        try:
           return Result.Ok(cls())
        except Exception as e:
            Result.Err(f"Failed to initialize Spotify client: {e.args[0]}") 


    def run(self, task: Result[ISpotifyTask[T], str]) -> Result[T, str]:
        """
        Runs a given task with the Spotify client.

        Args:
            task (ISpotifyTask[T]): The task to run.
        
        Returns:
            Result[T]: The result of the task if the operation was successful, or an error message otherwise.
        """
        
        return task.map(lambda task: task.run(self.__client))


    def __authorize(self) -> Result[Spotify, str]:
        """
        Authorizes with Spotify and returns a Spotify client.

        Returns:
            Result[Spotify, str]: A Spotify client if the authorization was successful, or an error message otherwise.
        """
        client_id: str | None = os.environ["SPOTIFY_CLIENT_ID"]
        if client_id is None:
            return Result.Err("SPOTIFY_CLIENT_ID not found in environment variables")

        secret_key: str | None = os.environ["SPOTIFY_CLIENT_SECRET"]
        if secret_key is None:
            raise Result.Err("SPOTIFY_CLIENT_ID or SPOTIFY_SECRET_KEY not found in environment variables")

        try:
            token: tk.RefreshingToken = tk.request_client_token(client_id, secret_key)
            spotify_client = tk.Spotify(token) 
            return Result.Ok(spotify_client)
        except Exception as e:
            return Result.Err(f"Failed to authorize with Spotify: {e}")