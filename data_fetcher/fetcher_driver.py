from data_fetcher.DataFetcher import DataFetcher
import json

fetcher = DataFetcher()
res = fetcher.run()
print(res)