import authorizer
import pandas as pd
import tekore as tk
import time
from tqdm import tqdm

def get_song_features(spotify: tk.Spotify, track_ids: list) -> list:
    retries = 0 
    while True: 
        try:
            return spotify.tracks_audio_features(track_ids)
        except tk.TooManyRequests:
            retries += 1
            print(f"ERROR: failed to retrieve audio features, retrying in {30 * retries} seconds...")
            time.sleep(30 * retries)
            pass


spotify = authorizer.authorize()
genres = spotify.recommendation_genre_seeds()

tracks = list()

for genre in tqdm(genres):
    recs = spotify.recommendations(genres = [genre], limit = 100)
    track_ids = [track.id for track in recs.tracks]

    for track in recs.tracks:
        song_features = get_song_features(spotify, track_ids) 

        tracks.append(song_features)

df = pd.DataFrame(tracks)
df.drop_duplicates(subset = "id", keep = "first", inplace = True)
df.to_csv("tracks.csv", index = False)
