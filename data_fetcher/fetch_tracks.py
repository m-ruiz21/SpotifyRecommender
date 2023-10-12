import authorizer
import pandas as pd
from tqdm import tqdm
from spotify_utils import runWithRetry

spotify = authorizer.authorize()
genres = runWithRetry(spotify.recommendation_genre_seeds) 

terms = set() 
for genre in tqdm(genres):
    recs = runWithRetry(spotify.recommendations, genres = [genre], limit = 100)

    for track in recs.tracks:
        terms.add(track.name)
        for artist in track.artists:
            terms.add(artist.name)

df = pd.DataFrame(terms)
df.to_csv("playlist_search_terms.csv", index = False)

print("\nDONE FETCHING TERMS\n")
print(f"Terms found: {len(terms)}")
