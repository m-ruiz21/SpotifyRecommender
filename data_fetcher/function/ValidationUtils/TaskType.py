import azure.functions as func
from Models.Result import Result
from ClientWrapper.Tasks.ISpotifyTask import ISpotifyTask
from ClientWrapper.Tasks.GetAvgPlaylistRating import GetAvgPlaylistRating
from ClientWrapper.Tasks.SearchPlaylists import SearchPlaylists

# create python enum
class TaskType:
    GET_AVG_PLAYLIST_RATING = "playlist_rating"
    SEACH_PLAYLISTS = "playlist_search"


def get_req_type(req: func.HttpRequest) -> Result[ISpotifyTask, str]: 
    req_type: str = req.route_params.get('task_type')

    match req_type:
        case TaskType.GET_AVG_PLAYLIST_RATING:
            return Result.Ok(GetAvgPlaylistRating.create_task(req))
        case TaskType.SEACH_PLAYLISTS:
            return Result.Ok(SearchPlaylists.create_task(req))
        case _:
            return Result.Err(f"Failed to retreive task type. Please provide a valid task type in route")