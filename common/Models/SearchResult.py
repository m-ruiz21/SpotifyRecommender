from common.Models.IApiModel import IApiModel
from typing import TypeVar, Generic 
import json
from common import Result

T = TypeVar('T', bound=IApiModel)
class SearchResult(Generic[T], IApiModel):
    def __init__(
            self,
            query: str,
            results: list[T]) -> None:

        self.query = query
        self.results = results
