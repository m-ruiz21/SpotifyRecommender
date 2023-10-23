import azure.functions as func
from Models.Result import Result
from ClientWrapper.Tasks.ISpotifyTask import ISpotifyTask
from ClientWrapper.Tasks.GetAvgPlaylistRating import GetAvgPlaylistRating

# create python enum
class TaskType:
    GET_AVG_PLAYLIST_RATING = "AVG_PLAYLIST_RATING"


def get_req_type(req: func.HttpRequest) -> Result[ISpotifyTask, str]: 
    req_type: str = req.route_params.get('task_param')

    match req_type:
        case TaskType.GET_AVG_PLAYLIST_RATING:
            return Result.Ok(GetAvgPlaylistRating(req))
        case _:
            return Result.Err(f"Failed to retreive task type. Please provide a valid task type in route")