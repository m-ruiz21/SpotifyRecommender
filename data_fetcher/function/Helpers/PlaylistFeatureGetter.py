from Models.Result import Result 
from Models.AudioFeatures import AudioFeatures
import tekore as tk
from tekore._client import Spotify
import logging
import time
import json

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
        logging.info(f"[PlaylistFeatureGetter]: Getting avg features of playlist with id: {playlist_id}")

        features = PlaylistFeatureGetter.__playlist_audio_features(playlist_id, client)
 
        avg_features = features.map(lambda features: PlaylistFeatureGetter.__get_avg_features(features))

        return avg_features 

    
    @staticmethod
    def __playlist_audio_features(playlist_id: str, client: Spotify) -> Result[list[tk.model.AudioFeatures], str]:
        """
        gets all the audio features of a playlist. 
        """
        logging.info(f"[PlaylistFeatureGetter]: Getting audio features of playlist with id: {playlist_id}")

        track_ids: Result[list[str], str] = PlaylistFeatureGetter.__get_playlist_track_ids(playlist_id, client)

        audio_features = track_ids.map(lambda track_ids: PlaylistFeatureGetter.__batch_fetch_audio_features(track_ids, client))

        return audio_features 
    
    
    @staticmethod
    def __get_playlist_track_ids(playlist_id: str, client: Spotify) -> Result[list[str], str]:
        """
        gets the tracks of a playlist.

        Args:
            playlist_id (str): The id of the playlist to get the tracks of.

        Returns:
            list of track ids
        """
        logging.info(f"Getting tracks of playlist with id: {playlist_id}")
        try:
            playlist_items = client.playlist_items(playlist_id, market='US') 

            playlist_items = client.all_items(playlist_items)

            track_ids = [item.track.id for item in playlist_items if item.track is not None]

            return Result.Ok(track_ids)
        except Exception as e:
            error_msg = e.args[0] if e.args else str(e) 
            return Result.Err(f"Failed to get playlist tracks: {error_msg}")


    @staticmethod
    def __batch_fetch_audio_features(track_ids: list[str], client: Spotify) -> Result[list[tk.model.AudioFeatures], str]:
        """
        gets the audio features of a list of tracks in batches of 50. 
        """
        logging.info(f"Fetching audio features of {len(track_ids)} tracks")

        chunks = [track_ids[i:i + 50] for i in range(0, len(track_ids), 50)]

        features = list[tk.model.AudioFeatures]()
        for i, chunk in enumerate(chunks):
            logging.info(f"Getting audio features: chunk {i+1} ...")

            chunk = [track_id for track_id in chunk if track_id is not None]
            try:

                audio_features = client.tracks_audio_features(chunk)

                audio_features = [feat for feat in audio_features if feat is not None] 

                features.extend(audio_features)

            except tk.ClientError as e: 
                error_msg = "tk.ClientError: " + json.dumps(e.response.content)

                retry_after = e.response.headers['Retry-After'] if e.response.headers['Retry-After'] else None 

                if retry_after:
                    if retry_after < 60:
                        logging.info(f"Client Error, retrying after {retry_after}")
                        time.sleep(retry_after)
                        return PlaylistFeatureGetter.__batch_fetch_audio_features(track_ids, client)
                
                    error_msg = f"Client Error, retry after {retry_after}"
                    
                return Result.Err(f"Failed to get audio features: {error_msg}")

            except Exception as e:
                error_msg = e.args[0] if e.args else str(e) 
                return Result.Err(f"Failed to get audio features: {error_msg}")

        logging.info("Successfully fetched audio features!")
        return Result.Ok(features) 
    

    @staticmethod
    def __get_avg_features(tracks_features: list[tk.model.AudioFeatures]) -> Result[AudioFeatures, str]:
        """
        gets the average features of a list of tracks.
        """ 
        logging.info(f"[PlaylistFeatureGetter]: Getting average features of {len(tracks_features)} tracks")

        avg_features = AudioFeatures()
        num_tracks = len(tracks_features)
        if num_tracks == 0: return Result.Ok(avg_features)

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