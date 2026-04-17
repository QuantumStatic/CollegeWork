from sortedcontainers import SortedList
from myfunctions import execute_this
import urllib.robotparser

import random
def clean_url(url:str,) -> str:
        
        parts = urllib.parse.urlparse(url)
        
        # Remove fragment and check if query is empty or starts with '?'
        query = '' if not parts.query or parts.query.startswith('?') else parts.query
        query = '/'.join(filter(bool, parts.query.split('/')))

        # Remove unnecessary slashes from the path
        
        path = '/'.join(filter(bool, parts.path.split('/')))
        cleaned_parts = parts._replace(fragment="", query=query, path=path)
        cleaned_url = urllib.parse.urlunparse(cleaned_parts)
        return cleaned_url

@execute_this
def test():
    a = {1, 2, 3}
    print(random.sample(sorted(a), k = 2))