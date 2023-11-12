import tekore as tk
from tekore._client import Spotify
from Models.Result import Result
import os
from typing import TypeVar 

class SpotifyClientFactory:

    @staticmethod
    def create_client() -> Result[Spotify, str]:
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