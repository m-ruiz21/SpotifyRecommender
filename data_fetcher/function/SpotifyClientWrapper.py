import tekore as tk
from tekore._client import Spotify
from Result import Result
import os
from dataclasses import dataclass
import json

class AudioFeatures:
    acousticness: float = 0.0 
    danceability: float = 0.0
    duration_ms: int = 0
    energy: float = 0.0
    instrumentalness: float = 0.0
    key: int = 0
    liveness: float = 0.0
    loudness: float = 0.0
    mode: int = 0
    speechiness: float = 0.0
    tempo: float = 0.0
    time_signature: int = 0
    valence: float = 0.0

    def to_json(self):
        return json.dumps(self.__dict__)


class spotify_client:
    __client: Spotify = None

    def __init__(self) -> None:
        """
        initializes the Spotify client wrapper.

        Returns:
            bool: True if the initialization was successful, False otherwise.
        """
        authorize_res = self.__authorize()
        if authorize_res.is_err():
            return 

        self.__client = authorize_res.unwrap() 


    def is_initialized(self) -> bool:
        """
        Returns True if the Spotify client wrapper is initialized, False otherwise.
        """
        return self.__client is not None


    def get_avg_playlist_features(self, playlist_id: str) -> Result[tk.model.AudioFeatures, str]:
        """
        gets the average features of a playlist.

        Args:
            playlist_id (str): The id of the playlist to get the features of.

        Returns:
            Result[tk.model.AudioFeatures, str]: The features of the playlist if the operation was successful, or an error message otherwise. 
        """
        features = self.__playlist_audio_features(playlist_id)
        avg_features = features.map(lambda features: self.__get_avg_features(features))
        return avg_features 


    def __playlist_audio_features(self, playlist_id: str) -> Result[list[tk.model.AudioFeatures], str]:
        """
        gets all the audio features of a playlist. 
        """
        track_ids: Result[list[str], str] = self.__get_playlist_track_ids(playlist_id)
        audio_features = track_ids.map(lambda track_ids: self.__client.tracks_audio_features(track_ids))

        return Result.Ok(audio_features)


    def __get_playlist_track_ids(self, playlist_id: str) -> Result[list[str], str]:
        """
        gets the tracks of a playlist.

        Args:
            playlist_id (str): The id of the playlist to get the tracks of.

        Returns:
        """
        try:
            playlist_items: tk.model.PlaylistTrackPaging = self.__client.playlist_items(playlist_id) 
            playlist_items = self.__client.all_items(playlist_items)
            
            track_ids = [item.track.id for item in playlist_items]
            return Result.Ok(track_ids)
        except Exception as e:
            return Result.Err(f"Failed to get playlist tracks: {e}")


    def __get_avg_features(self, tracks_features: list[tk.model.AudioFeatures]) -> Result[tk.model.AudioFeatures, str]:
        """
        gets the average features of a list of tracks.
        """ 
        avg_features = AudioFeatures()
    
        for track_features in tracks_features:
            avg_features.acousticness += track_features.acousticness
            avg_features.danceability += track_features.danceability
            avg_features.energy += track_features.energy
            avg_features.instrumentalness += track_features.instrumentalness
            avg_features.liveness += track_features.liveness
            avg_features.loudness += track_features.loudness
            avg_features.speechiness += track_features.speechiness
            avg_features.tempo += track_features.tempo
            avg_features.valence += track_features.valence
        
        avg_features.acousticness /= len(tracks_features)
        avg_features.danceability /= len(tracks_features)
        avg_features.energy /= len(tracks_features)
        avg_features.instrumentalness /= len(tracks_features)
        avg_features.liveness /= len(tracks_features)
        avg_features.loudness /= len(tracks_features)
        avg_features.speechiness /= len(tracks_features)
        avg_features.tempo /= len(tracks_features)
        avg_features.valence /= len(tracks_features)

        return Result.Ok(avg_features)


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
