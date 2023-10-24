import azure.functions as func
from Models.Result import Result

def get_search_query(req: func.HttpRequest) -> Result[str, str]:
    query = req.route_params.get('task_param')
    if query:
        return Result.Ok(query)
    else:
        return Result.Err(f"Failed to retreive search query. Please provide a valid search query")