from common.Models import AudioFeatures

class ModelData:
    def __init__(self, name: str, audio_features: AudioFeatures) -> None:
        self.name = name
        self.__dict__.update(audio_features.__dict__)