import azure.functions as func
import logging
from validation_utils import get_id
from SpotifyClientWrapper import spotify_client 

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="album_features_proxy/{album_id}")
def album_features_proxy(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    client =  spotify_client()
    if not client.is_initialized():
        logging.info(f'[ERROR]: Python HTTP trigger function returned error: Failed to create Spotify client\n Returned status code: 500')
        return func.HttpResponse("Failed to create Spotify client", status_code=500)
 
    album_id = get_id(req)
    album_features = album_id.map(lambda album_id: client.get_avg_playlist_features(album_id))
    if album_features.is_err():
        logging.info(f'[ERROR]: Python HTTP trigger function returned error: {album_features.unwrap()}\n Returned status code: 400')
        return func.HttpResponse(album_features.unwrap(), status_code=400)
    
    album_features_json = album_features.unwrap().to_json()
    return func.HttpResponse(album_features_json, status_code=200)