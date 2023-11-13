import pandas as pd
from data_fetcher.ProxyClient import ProxyClient
from common import Playlist, Result, AudioFeatures, ModelData
import os
import math 
import tqdm

class DataFetcher:

    client: Result[ProxyClient, str]
    terms: pd.DataFrame

    def __init__(self) -> None:
        self.client = ProxyClient.start()
        self.terms = self.fetch_terms()


    def run(self, term: str, limit: int) -> None: 
        '''
        runs the data fetching job for given term and limit 
        '''
        
        for row in self.terms.iterrows():

            search_amt = int(math.log(row['Count'], 2)) 
            result = self.search_and_write(
                term=row['Term'],
                limit=search_amt
            )

            if result.is_err(): print(result.error)


    def search_and_write(self, term: str, limit: int) -> Result[str, str]:
        '''
        searches for playlists wiht given term and writes the limit amount of playlists to csv file 
        '''

        playlists = self.fetch_playlists(term, limit)

        playlist_data = playlists.map(lambda playlists : self.fetch_playlists_data(playlists))

        job_result = playlist_data.map(lambda data: self.write_results_to_csv(data, 'data/playlists.csv'))
        return job_result

    
    def write_results_to_csv(self, data: list[ModelData], path: str) -> Result[str, str]:
        ''' 
        function that writes to csv file 

        Args:
            data (list[ModelData]): list of ModelData objects to write to csv
            path (str): path to csv file to write to
        
        Returns:
            Result[str, str]: "Success" / Error message for logging
        ''' 
        
        try:
            data_dicts = [obj.__dict__ for obj in data]
            df = pd.DataFrame(data_dicts)
            if not os.path.isfile(path):
                df.to_csv(path, index_label='id')
                return Result.Ok("Success")
            
            df_existing = pd.read_csv(path, index_col='id')
            start_id = df_existing.index.max() + 1
            df.index = pd.RangeIndex(start=start_id, stop=start_id + len(df))
            df_combined = pd.concat([df_existing, df])
            df_combined.to_csv(path, index_label='id')

            return Result.Ok("Success")
        except Exception as e:
            return Result.Err(f"Failed to write to csv: {e.args[0]}")


    def fetch_playlists_data(self, playlists: list[Playlist]) -> Result[list[ModelData], str]:
        """
        function that fetches data for given list of playlists 
        """
        results = list[ModelData]()
        for playlist in playlists:
            audio_features = self.fetch_playlist_data(playlist)
            if audio_features.is_err(): return Result.Err(audio_features.error)
            
            results.append(ModelData(playlist.name, audio_features.unwrap()))
            results.append(ModelData(playlist.description, audio_features.unwrap()))
        
        return Result.Ok(results)


    def fetch_playlists(self, term: str, limit=10) -> Result[list[Playlist], str]:
        """
        function that fetches playlists for given search term 
        """
        playlists = self.client.map(lambda client: client.get(f'playlist_search/{term}/{limit}'))
        playlists = playlists.map(lambda playlists: [Playlist.from_json(json) for json in playlists])
        for i, playlist in enumerate(playlists):
            if playlist.is_err(): return Result.Err(playlist.error) 
            playlists[i] = playlist.unwrap()

        return Result.Ok(playlists)


    def fetch_playlist_data(self, playlist: Playlist) -> Result[AudioFeatures, str]:
        """
        function that fetches audio features for given playlist
        """

        audio_features = self.client.map(lambda client: client.get(f'playlist_rating/{playlist.id}'))
        if audio_features is None: print('aaaaah none returned by get')

        audio_features = audio_features.map(lambda features: AudioFeatures.from_dict(features)) 

        return audio_features 


    def fetch_terms(self) -> pd.DataFrame:
        """
        function that fetches the terms from file
        """

        data = dict[str]() 
        with open('data/full_title.txt', 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                words = line.split()
                count = int(words[0])
                term = ' '.join(words[1:])
                data[term] = count

        df = pd.DataFrame(list(data.items()), columns=['Term', 'Count'])

        return df.sort_values('Count', ascending=False) 