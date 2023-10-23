from Models.Result import Result
import azure.functions as func
import os
import tekore as tk
from tekore._client import Spotify
from ClientWrapper.Tasks.ISpotifyTask import ISpotifyTask

def get_playlist_id(req: func.HttpRequest) -> Result[str, str]:
    album_id  = req.route_params.get('task_param')  
    if album_id:
        return Result.Ok(album_id)

    try:
        req_body = req.get_json()
    except ValueError:
        return Result.Err(f"Failed to retreive body from request. Please provide a valid album id in route or body")

    album_id = req_body.get('album_id')
    if album_id is None:
        return Result.Err(f"Failed to retreive album features. Please provide a valid album id")

    return Result.Ok(album_id)