import json

class IApiModel():
    """
    Base class / interface for all models returned by the API
    """    
    
    def to_json(self) -> str:
        return json.dumps(self.__dict__)