import json

class AudioFeatures:
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

    def to_json(self):
        return json.dumps(self.__dict__)