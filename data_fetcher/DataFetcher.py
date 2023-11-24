import pandas as pd
from data_fetcher.ProxyClient import ProxyClient
from common import Playlist, Result, AudioFeatures, ModelData
import os
import math 
import random
import time
from tqdm import tqdm

class DataFetcher:

    client: Result[ProxyClient, str]
    terms: pd.DataFrame

    pbar: tqdm

    def __init__(self) -> None:
        self.client = ProxyClient.start()
        print("[DataFetcher]: Client has been started")

        self.terms = self.fetch_terms()
        print("[DataFetcher]: Terms have been loaded")


    def run(self, path: str, offset: int = 0) -> None: 
        '''
        runs the data fetching job for given term and limit 
        '''

        self.pbar = tqdm(total=self.terms.shape[0])
        self.pbar.update(offset)
        for i, row in self.terms.iterrows(): 
            if i < offset: continue 
            
            search_amt = int(math.log(row['Count'], 2) / 2)
            result = self.search_and_write(
                term=row['Term'],
                limit=search_amt,
                path=path
            )

            if result.is_err():
                print(f"\tError index: {i}")
                result.unwrap()     # throws error 

            self.pbar.update(1)
        
        print("Done!")


    def search_and_write(self, term: str, limit: int, path: str) -> Result[str, str]:
        '''
        searches for playlists wiht given term and writes the limit amount of playlists to csv file 
        '''
        self.pbar.set_description(f"{term}: Fetching Playlists with query '{term}'")
        playlists = self.fetch_playlists(term, limit=limit)

        self.pbar.set_description(f"{term}: Fetching Playlist Data for retreived playlists...")
        playlist_data = playlists.map(lambda playlists : self.fetch_playlists_data(playlists))

        self.pbar.set_description(f"{term}: Writing Playlist Data to csv...")
        job_result = playlist_data.map(lambda data: self.write_results_to_csv(data, path))
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
                df.to_csv(path, index_label='idx')
                return Result.Ok("Success")
            
            df_existing = pd.read_csv(path, index_col='idx')
            start_idx = df_existing.index.max() + 1
            df.index = pd.RangeIndex(start=start_idx, stop=start_idx + len(df))
 
            df_combined = pd.concat([df_existing, df])
            df_combined = df_combined.drop_duplicates(subset=['id'], keep='first')
            df_combined.to_csv(path, index_label='idx')

            return Result.Ok("Success")
        except Exception as e:
            return Result.Err(f"Failed to write to csv: {e.args[0]}")


    def fetch_playlists_data(self, playlists: list[Playlist]) -> Result[list[ModelData], str]:
        """
        function that fetches data for given list of playlists 
        """

        results = list[ModelData]()
        total = len(playlists)
        for id, playlist in enumerate(playlists):
            self.pbar.set_description(f"Fetching data for retrieved playlist {id+1}/{total}")
            audio_features = self.fetch_playlist_data(playlist)

            if audio_features.is_err(): return Result.Err(audio_features.error)
            if not audio_features.value: continue   # checks if no audio features found 
            
            results.append(ModelData(playlist.id, playlist.name, audio_features.unwrap()))
        
        return Result.Ok(results)


    def fetch_playlists(self, term: str, limit: int) -> Result[list[Playlist], str]:
        """
        function that fetches playlists for given search term 
        """
        playlists = self.client.map(lambda client: client.get(f'playlist_search/{term}/{limit}'))
        playlists = playlists.map(lambda playlists: Result.Ok([Playlist.from_json(json) for json in playlists])) 

        playlists = playlists.map(
            lambda playlists:
            Result.Ok([playlist.value for playlist in playlists])
            if all([playlist.is_ok() for playlist in playlists]) else Result.Err("Error in playlist")
        )

        return playlists 


    def fetch_playlist_data(self, playlist: Playlist) -> Result[AudioFeatures, str]:
        """
        function that fetches audio features for given playlist
        """

        audio_features = self.client.map(lambda client: client.get(f'playlist_features/{playlist.id}'))

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