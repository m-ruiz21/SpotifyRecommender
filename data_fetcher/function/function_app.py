import azure.functions as func
import logging
from Models.Result import Result
from Client.SpotifyClientFactory import SpotifyClientFactory
from Helpers.PlaylistFeatureGetter import PlaylistFeatureGetter
from Helpers.PlaylistSearcher import PlaylistSearcher
from Utils.ErrorUtils import log_and_return_error 
import tekore as tk
from Utils.ErrorUtils import get_ip

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
spotify_client = SpotifyClientFactory.create_client()

@app.route(route="playlist_search/{search_query}/{limit}")
def search_playlist(req: func.HttpRequest) -> func.HttpResponse:
    """
    Searches for playlists with the given search query.

    Args:
        search_query (str): The search query to search for.
        limit (Optional<int>): The maximum number of results to return.

    Returns:
        Search result as list of Playlist Objects called "SearchResult"
    """

    logging.info('Python HTTP trigger function processed a request to retrieve playlist rating.')
    logging.info(f"IP Address: {get_ip()}") 

    search_query = req.route_params.get('search_query')
    limit = int(req.route_params.get('limit'))   # optional param

    if not search_query:
        return log_and_return_error(
            result=Result.Err(f"Failed to retreive search query. Please provide a valid search query"), 
            code=400)

    search_result = spotify_client.map(lambda client: PlaylistSearcher.search(search_query, client, limit))

    if search_result.is_err(): 
        return log_and_return_error(result=search_result, code=500)

    result_json = search_result.value.to_json()
    return func.HttpResponse(result_json, status_code=200)


@app.route(route="playlist_features/{playlist_id}")
def get_playlist_features(req: func.HttpRequest) -> func.HttpResponse:
    """
    Gets the average features of a playlist. 

    Args:
        playlist_id: The id of the playlist to get the features of. 
    """  
    
    logging.info('Python HTTP trigger function processed a request to retrieve playlist features.')
    logging.info(f"IP Address: {get_ip()}") 

    playlist_id = req.route_params.get('playlist_id')
    if not playlist_id:
        return log_and_return_error(
            result=Result.Err(f"Failed to retreive playlist id. Please provide a valid playlist id"), 
            code=400)

    playlist_features = spotify_client.map(
            lambda spotify_client:
            PlaylistFeatureGetter.get_avg_playlist_features(playlist_id, spotify_client)
        )

    if playlist_features.is_err():
        return log_and_return_error(result=playlist_features, code=400)

    result_json = playlist_features.unwrap().to_json()
    return func.HttpResponse(result_json, status_code=200)