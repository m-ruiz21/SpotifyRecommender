from Models.IApiModel import IApiModel
from typing import Optional

class Playlist(IApiModel):
    id: str = "" 
    name: str = ""
    description: Optional[str] = None