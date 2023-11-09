from common.Models.IApiModel import IApiModel
from typing import TypeVar
import json

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