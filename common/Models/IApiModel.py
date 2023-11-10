import json
from abc import abstractclassmethod
from common import Result

class IApiModel():
    """
    Base class / interface for all models returned by the API
    """    
    
    def to_json(self) -> str:
        """
        Converts the model to a JSON string. 
        """
        return json.dumps(self.__dict__)
    

    def __str__(self) -> str:
        return json.dumps(self.__dict__, indent=4)