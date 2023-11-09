import pandas as pd
from data_fetcher.ProxyClient import ProxyClient
from common import Playlist, Result, AudioFeatures


class DataFetcher:

    client: Result[ProxyClient, str]
    terms: pd.DataFrame

    def __init__(self) -> None:
        self.client = ProxyClient.start()
        self.terms = self.fetch_terms()


    def fetch_playlists_data(self):
        for index, row in self.terms.iterrows():
            term = row['Term']
            count = row['Count']
            playlists = self.fetch_playlists(term)


    def fetch_playlists(self, term: str) -> Result[Playlist, str]:
        playlists = self.client.map(lambda client: client.get(f'playlist_search/{term}'))
        playlists = playlists.map(lambda playlists: [Playlist.from_json(json) for json in playlists])
        for i, playlist in enumerate(playlists):
            if playlist.is_err(): return Result.Err(playlist.error) 
            playlists[i] = playlist.unwrap()

        return Result.Ok(playlists)


    def fetch_playlist_data(self, playlist: Playlist) -> Result[AudioFeatures, str]:
        audio_features = self.client.map(lambda client: client.get(f'playlist_rating/{playlist.id}'))
        audio_features = audio_features.map(lambda features: AudioFeatures.from_dict(features)) 

        return audio_features 


    def fetch_terms(self) -> pd.DataFrame:
        data = dict[str]() 
        with open('data/full_title.txt', 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                words = line.split()
                count = int(words[0])
                term = ' '.join(words[1:])
                data[term] = count

        df = pd.DataFrame(list(data.items()), columns=['Term', 'Count'])

        return df.sort_values('Count', ascending=False)