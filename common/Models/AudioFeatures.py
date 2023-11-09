import json
from common.Models.IApiModel import IApiModel
from common import Result

class AudioFeatures(IApiModel):
    acousticness: float = 0.0 
    danceability: float = 0.0
    duration_ms: int = 0
    energy: float = 0.0
    instrumentalness: float = 0.0
    key: int = 0
    liveness: float = 0.0
    loudness: float = 0.0
    mode: int = 0
    speechiness: float = 0.0
    tempo: float = 0.0
    time_signature: int = 0
    valence: float = 0.0


    def __init__(
            self,
            acousticness: float,
            danceability: float,
            duration_ms: int,
            energy: float,
            instrumentalness: float,
            key: int,
            liveness: float,
            loudness: float,
            mode: int,
            speechiness: float,
            tempo: float,
            time_signature: int,
            valence: float) -> None:
        
        self.acousticness = acousticness
        self.danceability = danceability
        self.duration_ms = duration_ms
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.key = key
        self.liveness = liveness
        self.loudness = loudness
        self.mode = mode
        self.speechiness = speechiness
        self.tempo = tempo
        self.time_signature = time_signature
        self.valence = valence


    @classmethod
    def from_json(cls, json_obj: str) -> Result['AudioFeatures', str]:
        """
        Creates model from given json string. 
        """
        try:
            json_dict = json.loads(json_obj) 
        except Exception as e:
            return Result.Err(f"Failed to parse json: {e.args[0]}")
        

        audio_features = cls.from_dict(json_dict)
        return audio_features
    
 
    def from_dict(cls, json_dict) -> Result['AudioFeatures', str]:
        try:
            audio_features = cls(
                json_dict["acousticness"],
                json_dict["danceability"],
                json_dict["duration_ms"],
                json_dict["energy"],
                json_dict["instrumentalness"],
                json_dict["key"],
                json_dict["liveness"],
                json_dict["loudness"],
                json_dict["mode"],
                json_dict["speechiness"],
                json_dict["tempo"],
                json_dict["time_signature"],
                json_dict["valence"]
            )

            return Result.Ok(audio_features)
        except Exception as e:
            return Result.Err(f"Failed to parse json: {e.args[0]}")
