from data_fetcher.DataFetcher import DataFetcher
import json

fetcher = DataFetcher()
res = fetcher.run('data/playlist_features.csv', offset=1205)