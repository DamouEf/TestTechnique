from unittest import result
from urllib import response
import requests
from django.conf import settings
import logging

# This retrieves a Python logging instance (or creates it)
logger = logging.getLogger(__name__)

# Constants 
BASE_URL = settings.BASE_URL_PAGE_SPEED

class PageSpeed:

    """
    This class PageSpeed is a connector that allow user to use PageSpeed Insights APIs
    for more details about PageSpeed Insights check : (https://developers.google.com/speed/docs/insights/v5/about)
    """

    def __init__(self) -> None:
        pass

    @classmethod
    def runpagespeed(cls, url_to_analyse="https://www.voici.fr", category="PERFORMANCE") -> dict:
        """
        This function is used to consume GET runPagespeed endpoint of PageSpeed Insights APIs
        """

        url: str = str(f'{BASE_URL}runPagespeed?url={url_to_analyse}&category={category}')
        
        # get response
        response: dict = PageSpeed.create_request(method="GET", url=url)

        if not response or not(response.status_code == 200):
            logger.info("response from runPagespeed endpoint of PageSpeed Insights APIs Failed!")
            return None

        # parse response
        parsed_data: dict = PageSpeed.parse_data(data=response.json())
        return parsed_data 

    @classmethod
    def create_request(cls, method, url, payload={}, headers={}):
        """
            This method creates a HTTP request, from given args
        """
        logger.info(f"Create {method} http request")
        if not headers:
            headers = {'Content-Type': 'application/json'}
        response = requests.request(
            method=method,
            url=url,
            verify=False,
            data=payload,
            headers=headers
        )

        logger.info(f"status code : {response.status_code}")
        return response
    
    @classmethod
    def parse_data(cls, data: dict) -> dict:
        """
        This function will takes the runPagespeed endpoint response from PageSpeed Insights API and extarct the data of the performance

        input : 
            data : dict

        return :
            dict 
            {
                * performance_score : int
                * interactive_score : int | Time to interactive is the amount of time it takes for the page to become fully interactive.
                * speed_index : int | "Speed Index shows how quickly the contents of a page are visibly populated.
                * javascript_execution_time | Consider reducing the time spent parsing, compiling, and executing JS.
            } 
        """
        logger.info("parse data start !")
        result: dict = dict()

        result["performance_score"] = data.get("lighthouseResult", {}).get("categories", {}).get("performance", {}).get("score")
        result["interactive_score"] = data.get("lighthouseResult", {}).get("audits", {}).get("interactive", {}).get("score")
        result["speed_index"] = data.get("lighthouseResult", {}).get("audits", {}).get("speed-index", {}).get("score")
        result["javascript_execution_time"] = data.get("lighthouseResult", {}).get("audits", {}).get("bootup-time", {}).get("displayValue")

        return result