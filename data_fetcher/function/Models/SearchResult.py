from Models.Playlist import Playlist
from Models.IApiModel import IApiModel
from typing import Generic, TypeVar
import json

T = TypeVar('T')
class SearchResult(IApiModel):
    def __init__(
            self,
            query: str,
            results: list[IApiModel]) -> None:

        self.query = query
        self.results = results

    
    def to_json(self) -> str:
        json_results = [result.to_json() for result in self.results]
        return json.dumps(json_results)