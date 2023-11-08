import os
from dotenv import load_dotenv
import requests
import random
from common.Models.Result import Result

BASE_URL = ".azurewebsites.net/api/"

class ProxyClient:
    '''
    Handles the communication with the proxy server. 
    '''

    __proxy_names = list[str]()

    def __init__(self):
        self.__get_proxy_names()


    def get(self, endpoint: str) -> Result[str, str]:
        '''
        Sends a GET request to the proxy server.
        '''
        proxy_name = self.__select_proxy()
        try:
            response = requests.get("https://" + proxy_name + BASE_URL + endpoint)
            if response.status_code == 200:
                return Result.Ok(response.text)
        except Exception as e:
            return Result.Err(e.args[0])

    
    def __select_proxy(self) -> Result[str, str]:
        '''
        Selects a random proxy server to use.
        '''        
        proxy_num = random.randint(0, len(self.__proxy_names))
        return self.__proxy_names[proxy_num]


    def __get_proxy_names(self) -> None:
        load_dotenv()
        num_proxies: int = int(os.getenv("NUM_PROXIES"))
        for i in range(num_proxies):
            self.__proxy_names.append(os.getenv("PROXY_" + str(i+1)))