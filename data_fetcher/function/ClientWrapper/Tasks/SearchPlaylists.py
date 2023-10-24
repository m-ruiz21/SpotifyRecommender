from ClientWrapper.Tasks.ISpotifyTask import ISpotifyTask
from Models.AudioFeatures import AudioFeatures
from tekore._client import Spotify
import azure.functions as func
from Models.Result import Result 

class SearchPlaylists(ISpotifyTask[str]):
    request: func.HttpRequest = None 

    def __init__(self, request: func.HttpRequest):
        super().__init__(request)
