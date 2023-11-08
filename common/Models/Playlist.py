from Models.IApiModel import IApiModel
from typing import Optional
from tekore.model import SimplePlaylist

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
    def from_simple_playlist(cls, simple_playlist: SimplePlaylist) -> 'Playlist': 
        return cls(
                simple_playlist.id, 
                simple_playlist.name, 
                simple_playlist.description
            )