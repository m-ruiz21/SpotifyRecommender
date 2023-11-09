from data_fetcher.DataFetcher import DataFetcher
import json

fetcher = DataFetcher()
playlists = fetcher.fetch_playlists("rock")
playlist_data = playlists.map(lambda playlists : fetcher.fetch_playlist_data(playlists[0]))
print(playlist_data) 