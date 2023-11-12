import logging
from Models.Result import Result
import azure.functions as func

def log_and_return_error(result: Result, code: int) -> func.HttpResponse:
    logging.error(f'[ERROR]: Python HTTP trigger function returned error: \"{result.error}\" - Returned status code: 400')
    return func.HttpResponse(result.error, status_code=code)