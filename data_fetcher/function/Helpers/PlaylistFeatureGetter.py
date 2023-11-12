from Models.Result import Result 
from Models.AudioFeatures import AudioFeatures
import tekore as tk
from tekore._client import Spotify
import azure.functions as func

class PlaylistFeatureGetter():
    """
    Helper to get the average features of a playlist.
    """

    @staticmethod
    def get_avg_playlist_features(playlist_id: str, client: Spotify) -> Result[AudioFeatures, str]:
        """
        gets the average features of a playlist.

        Args:
            playlist_id (str): The id of the playlist to get the features of.

        Returns:
            Result[tk.model.AudioFeatures, str]: The features of the playlist if the operation was successful, or an error message otherwise. 
        """
        features = PlaylistFeatureGetter.__playlist_audio_features(playlist_id, client)
        avg_features = features.map(lambda features: PlaylistFeatureGetter.__get_avg_features(features))
        return avg_features 


    @staticmethod
    def __get_avg_features(tracks_features: list[tk.model.AudioFeatures]) -> Result[AudioFeatures, str]:
        """
        gets the average features of a list of tracks.
        """ 
        avg_features = AudioFeatures()
        num_tracks = len(tracks_features)
    
        for track_features in tracks_features:
            avg_features.acousticness += track_features.acousticness
            avg_features.danceability += track_features.danceability
            avg_features.duration_ms += track_features.duration_ms
            avg_features.energy += track_features.energy
            avg_features.instrumentalness += track_features.instrumentalness
            avg_features.key += track_features.key
            avg_features.liveness += track_features.liveness
            avg_features.loudness += track_features.loudness
            avg_features.mode += track_features.mode
            avg_features.speechiness += track_features.speechiness
            avg_features.tempo += track_features.tempo
            avg_features.time_signature += track_features.time_signature
            avg_features.valence += track_features.valence
        
        avg_features.acousticness /= num_tracks 
        avg_features.danceability /= num_tracks
        avg_features.duration_ms /= num_tracks
        avg_features.energy /= num_tracks
        avg_features.instrumentalness /= num_tracks
        avg_features.key /= num_tracks
        avg_features.liveness /= num_tracks
        avg_features.loudness /= num_tracks
        avg_features.mode /= num_tracks
        avg_features.speechiness /= num_tracks
        avg_features.tempo /= num_tracks
        avg_features.time_signature /= num_tracks
        avg_features.valence /= num_tracks

        return Result.Ok(avg_features)


    @staticmethod
    def __playlist_audio_features(playlist_id: str, client: Spotify) -> Result[list[tk.model.AudioFeatures], str]:
        """
        gets all the audio features of a playlist. 
        """
        track_ids: Result[list[str], str] = PlaylistFeatureGetter.__get_playlist_track_ids(playlist_id, client)
 
        audio_features = track_ids.map(lambda track_ids: PlaylistFeatureGetter.__batch_fetch_audio_features(track_ids, client))

        return audio_features 


    @staticmethod
    def __batch_fetch_audio_features(track_ids: list[str], client: Spotify) -> Result[list[tk.model.AudioFeatures], str]:
        """
        gets the audio features of a list of tracks in batches of 50. 
        """
        chunks = [track_ids[i:i + 50] for i in range(0, len(track_ids), 50)]
        features = list[tk.model.AudioFeatures]()
        for chunk in chunks:
            try:
                features.extend(client.tracks_audio_features(chunk))
            except Exception as e:
                return Result.Err(f"Failed to get audio features: {e.args[0]}")

        return Result.Ok(features)


    @staticmethod
    def __get_playlist_track_ids(playlist_id: str, client: Spotify) -> Result[list[str], str]:
        """
        gets the tracks of a playlist.

        Args:
            playlist_id (str): The id of the playlist to get the tracks of.

        Returns:
        """
        try:
            playlist_items: tk.model.PlaylistTrackPaging = client.playlist_items(playlist_id) 
            playlist_items = client.all_items(playlist_items)
            
            track_ids = [item.track.id for item in playlist_items]
            return Result.Ok(track_ids)
        except Exception as e:
            return Result.Err(f"Failed to get playlist tracks: {e}")