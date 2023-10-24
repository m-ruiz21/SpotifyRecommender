import azure.functions as func
import logging
from ValidationUtils.TaskType import get_req_type
from ValidationUtils.TaskType import ISpotifyTask
from ClientWrapper.Client import SpotifyClient 

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="album_features_proxy/{task_type}/{task_param}")
def album_features_proxy(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    spotify_client = SpotifyClient.start()
    task: ISpotifyTask = get_req_type(req) 
    task_result = spotify_client.map(lambda client: client.run(task))
    
    if task_result.is_err():
        logging.info(f'[ERROR]: Python HTTP trigger function returned error: {task_result.error}\n Returned status code: 400')
        return func.HttpResponse(task_result.error, status_code=400)
    
    result_json = task_result.unwrap().to_json()
    return func.HttpResponse(result_json, status_code=200)