from common.Models.IApiModel import IApiModel
from typing import Optional
from tekore.model import SimplePlaylist
from common import Result
import json

class Playlist(IApiModel):
    def __init__(
            self,
            id: str, 
            name: str, 
            description: Optional[str]) -> None:

        self.id = id
        self.name = name
        self.description = description


    @classmethod
    def from_json(obj, json_obj: str) -> Result['Playlist', str]:
        data = json.loads(json_obj)
        
        try:
            playlist = obj(
                data["id"], 
                data["name"], 
                data["description"]
            )

            return Result.Ok(playlist)
        except KeyError as e:
            return Result.Err(f"Failed to parse json: {e.args[0]}")


    @classmethod
    def from_simple_playlist(cls, simple_playlist: SimplePlaylist) -> 'Playlist': 
        return cls(
                simple_playlist.id, 
                simple_playlist.name, 
                simple_playlist.description
            )