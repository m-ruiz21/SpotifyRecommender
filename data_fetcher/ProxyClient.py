import os
from dotenv import load_dotenv
import requests
import random
from common.Models.Result import Result
from typing import TypeVar, Type

BASE_URL = ".azurewebsites.net/api/"
ProxyClient = TypeVar('ProxyClient')

class ProxyClient:
    '''
    Handles the communication with the proxy server. 
    '''

    __proxy_names = list[str]()

    def __init__(self):
        proxy_names = self.__get_proxy_names()
        if proxy_names.is_err(): raise Exception(proxy_names.error)
        self.__proxy_names = proxy_names.unwrap()


    @classmethod
    def start(cls: Type[ProxyClient]) -> Result[ProxyClient, str]:
        """
        Safely initializes the client without exception.

        Returns:
            Result[ProxyClient, str]: The client if the initialization was successful, or an error message otherwise.
        """
        try:
           return Result.Ok(cls())
        except Exception as e:
            Result.Err(f"Failed to initialize client: {e.args[0]}") 


    def get(self, endpoint: str) -> Result[str, str]:
        '''
        Sends a GET request to the proxy server.

        Args:
            endpoint (str): The endpoint to send the request to.
        
        Returns:
            Result[str, str]: The response body of the request. 
        '''
        proxy_name = self.__select_proxy()

        try:
            response = requests.get("https://" + proxy_name + BASE_URL + endpoint)
            if response.status_code == 200:
                return Result.Ok(response.json())
        except Exception as e:
            return Result.Err(e.args[0])

    
    def __select_proxy(self) -> str:
        '''
        Selects a random proxy server to use.

        Returns:
            Result[str, str]: The url of the chosen proxy server.
        '''   
        proxy_num = random.randint(0, len(self.__proxy_names)-1)
        return self.__proxy_names[proxy_num]


    def __get_proxy_names(self) -> Result[list[str], str]:
        '''
        Gets the names of the proxy servers from the .env file and loads them into __proxy_names.
        '''
        load_dotenv()
        
        num_proxies: str = os.getenv("NUM_PROXIES")
        if not num_proxies: return Result.Err("NUM_PROXIES not found in .env file.")

        num_proxies = int(num_proxies)
        proxies: list[str] = list[str]()
        for i in range(num_proxies):
            proxy_name = os.getenv("PROXY_" + str(i+1))
            if not proxy_name: return Result.Err("PROXY_" + str(i+1) + " not found in .env file.")
            
            proxies.append(proxy_name)

        return Result.Ok(proxies)