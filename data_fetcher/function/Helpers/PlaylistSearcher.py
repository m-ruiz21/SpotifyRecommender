from Client.SpotifyClientFactory import SpotifyClientFactory
from Models.AudioFeatures import AudioFeatures
from tekore._client import Spotify
import azure.functions as func
from Models.Result import Result 
from Models.SearchResult import SearchResult 
from typing import Generator
from Models.Playlist import Playlist

class PlaylistSearcher():
    """
    Collection of helper functions to help search for playlists    
    """

    @staticmethod 
    def search(search_query: str, client: Spotify, limit: int = 10) -> Result[SearchResult, str]:
        """
        Searches for playlists with the given search query and converts the results to a list of Playlists.

        Args:
            search_query: The search query to search for.
            client: The Spotify client to use.

        Returns:
            A Result with a list of Playlists if successful, otherwise a Result with an error message. 
        """

        search_res = PlaylistSearcher.__send_search_query(search_query, client, limit)
        playlists = search_res.map(lambda search_res: PlaylistSearcher.__generator_to_list(search_res[0]))
        search_results = playlists.map(lambda playlists: Result.Ok(SearchResult(search_query, playlists)))
        return search_results


    @staticmethod
    def __send_search_query(search_query, client: Spotify, limit) -> Result[list[Playlist], str]:
        """
        Sends the search query to Spotify and returns the result.
        """

        try:
            search_res = client.search(search_query, types=('playlist',), limit=limit)

            return Result.Ok(search_res)
        except Exception as e:
            return Result.Err(f"Failed to search for playlist: {e.args[0]}")


    @staticmethod
    def __generator_to_list(generator: Generator) -> Result[list[Playlist], str]:
        """
        Adaptor for spotify client's generator to a list of Playlists.
        """ 
        res = [Playlist.from_simple_playlist(playlist) for playlist in generator.items]
        return Result.Ok(res)