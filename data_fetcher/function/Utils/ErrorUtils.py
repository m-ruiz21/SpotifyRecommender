import logging
from Models.Result import Result
import azure.functions as func
import requests

def log_and_return_error(result: Result, code: int) -> func.HttpResponse:
    logging.error(f'[ERROR]: Python HTTP trigger function returned error: \"{result.error}\" - Returned status code: {code}')
    return func.HttpResponse(result.error, status_code=code)


def get_ip() -> str:
    try:
        response = requests.get('https://api.ipify.org') 
        return response.text
    except Exception as e:
        logging.error(f'Error getting ip: {e}')
        return 'Error getting ip'