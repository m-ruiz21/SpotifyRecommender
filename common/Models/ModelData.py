from common.Models import AudioFeatures

class ModelData:
    def __init__(self, id: str, name: str, audio_features: AudioFeatures) -> None:
        self.id = id
        self.name = name
        self.__dict__.update(audio_features.__dict__)