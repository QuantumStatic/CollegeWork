from urllib3.exceptions import InsecureRequestWarning
import warnings
import requests
import concurrent.futures
from typing import Union

# Suppress only the single warning from urllib3 needed.
warnings.filterwarnings('ignore', 'Unverified HTTPS request', InsecureRequestWarning)


def get_response(url: str, timeout:int=5) -> requests.Response:
    """Get the response from the url"""
    return requests.get(url, timeout=timeout, verify=False)


def _parallel_get_response(url: str) -> tuple[str, Union[requests.Response, None]]:
    """This is a wrapper to get_response to be used in the concurrent.futures module"""
    try:
        return (url, get_response(url))
    except Exception:
        return (url, None)


def multi_get_response(url_list: list[str], timeout: int = 20) -> list[tuple[str, requests.Response]]:
    """Get the response from the list of urls"""

    # Initialise the executor
    with concurrent.futures.ProcessPoolExecutor() as executor:
        processes = [executor.submit(_parallel_get_response, url) for url in url_list]

        # Yield the results as they are completed rather than the order they were given
        try:
            for process in concurrent.futures.as_completed(processes, timeout=timeout):
                yield process.result()
        except concurrent.futures.TimeoutError:
            yield None


