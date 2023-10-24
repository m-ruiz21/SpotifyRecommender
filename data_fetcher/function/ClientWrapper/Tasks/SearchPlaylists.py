from ClientWrapper.Tasks.ISpotifyTask import ISpotifyTask
from Models.AudioFeatures import AudioFeatures
from tekore._client import Spotify
import azure.functions as func
from Models.Result import Result 
from Models.Playlist import Playlist
from ValidationUtils.SearchQuery import get_search_query
from typing import Generator

class SearchPlaylists(ISpotifyTask[Playlist]):
    """
    Task to search for 10 playlists using given search query.
    """

    request: func.HttpRequest = None 

    def __init__(self, request: func.HttpRequest):
        super().__init__(request)


    def run(self, client: Spotify) -> Result[Playlist, str]:
        search_query = get_search_query(self.request)
        return search_query.map(lambda search_query: self.__search(search_query, client))


    def __search(self, search_query, client: Spotify) -> Result[list[Playlist]]:
        """
        Searches for playlists with the given search query and converts the results to a list of Playlists.

        Args:
            search_query: The search query to search for.
            client: The Spotify client to use.

        Returns:
            A Result with a list of Playlists if successful, otherwise a Result with an error message. 
        """

        search_res = self.__send_search_query(search_query, client)
        playlists = search_res.map(lambda search_res: self.__generator_to_list(search_res.playlists, client))
        return playlists


    def __send_search_query(self, search_query, client: Spotify) -> Result[list[Playlist]]:
        """
        Sends the search query to Spotify and returns the result.
        """

        try:
            search_res = client.search(search_query, types='playlist', limit=10)
            return Result.Ok(search_res)
        except Exception as e:
            return Result.Err(f"Failed to search for playlist: {e.args[0]}")


    def __generator_to_list(self, generator: Generator, client: Spotify) -> list[Playlist]:
        """
        Adaptor for spotify client's generator to a list of Playlists.
        """

        res = client.all_items(generator)
        res = [Playlist.from_simple_playlist(playlist) for playlist in res]
        return res