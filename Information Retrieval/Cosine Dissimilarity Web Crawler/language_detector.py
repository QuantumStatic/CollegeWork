import concurrent.futures
import bs4
import langid
import requests

import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.filterwarnings('ignore', 'Unverified HTTPS request', InsecureRequestWarning)

def detect_language_url(url:str) -> str:
    """Detect the language of a page represented by the url"""
    try:
        request = requests.get(url, timeout=10, verify=False)
    except Exception:
        return 'not found'

    try:
        return langid.classify(request.text)[0]
    except Exception:
        return 'Not found'

def detect_language_response(text:str) -> str:
    """Detect the language of a page represented by the response object"""
    try:
        return langid.classify(text)[0]
    except Exception:
        return None


def _parallel_detect_language_response(url, response) -> tuple[bs4.BeautifulSoup, str]:
    try:
        response.url = url
        return (response, detect_language_response(response.text))
    except Exception:
        return (response, None)

def multi_detect_language_response(reponses:list, timeout:int=25) -> list[tuple[requests.Response, str]]:
    """Detect the language of a list of response objects"""

    with concurrent.futures.ProcessPoolExecutor() as executor:
        processes = [executor.submit(_parallel_detect_language_response, url, response) for url, response in reponses]

        # In this case we are using as_completed because we want to return the results as they finish
        for process in concurrent.futures.as_completed(processes, timeout=timeout):
            yield process.result()


def _parallel_detect_language_url(url) -> None:
    try:
        return (url, detect_language_url(url))
    except Exception:
        return (url, 'Not found')

def multi_detect_language_url(url_list:list[str]) -> list:

    """Detect the language of a list of urls"""
    with concurrent.futures.ProcessPoolExecutor() as executor:
        processes = [executor.submit(_parallel_detect_language_url, url) for url in url_list]

        for process in concurrent.futures.as_completed(processes):
            yield process.result()
