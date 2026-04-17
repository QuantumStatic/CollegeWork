import concurrent.futures
import urllib.robotparser
import urllib.parse
import pathlib
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
from tldextract import TLDExtract
import os


# Suppress only the single warning from urllib3 needed.
warnings.filterwarnings('ignore', 'Unverified HTTPS request', InsecureRequestWarning)

# Declare the path where robots.txt is stored
ROBOT_STORE = pathlib.Path("robots_store/")
os.makedirs(ROBOT_STORE, exist_ok=True)

extractor = TLDExtract()

def get_robots_txt(url, skip_url_processing=False):
    """Return a robotparser object for the given url"""

    if url is None or url.strip() == "":
        return urllib.robotparser.RobotFileParser()

    # if the function is called recursively no need to process the url again to extract domain name
    if not skip_url_processing:
        parsed_url = urllib.parse.urlsplit(url)
        domain = extractor.extract_urllib(parsed_url).fqdn
    else:
        domain = url

    try:
        # Look for the file in our store first, if it exists, use it
        with open(ROBOT_STORE / f"{domain}.txt", "r", encoding='utf-8') as file:
            # 
            file_text = file.read()
            new_rp = urllib.robotparser.RobotFileParser()
            new_rp.parse(file_text.splitlines())
            new_rp.domain = domain
            return new_rp
    except FileNotFoundError:
        # If the file does not exist, download it and store it
        try:
            req = requests.get(f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt", timeout=7, allow_redirects=True, verify=False)
        except Exception:
            return urllib.robotparser.RobotFileParser()
        else:
            with open(ROBOT_STORE / f"{domain}.txt" , "w", encoding='utf-8') as file:
                try:
                    file.write(req.content.decode('utf-8'))
                except UnicodeDecodeError:
                    new_rp = urllib.robotparser.RobotFileParser()
                    new_rp.domain = domain
                    return new_rp
            
            return get_robots_txt(domain, skip_url_processing=True)
    except Exception:
        return urllib.robotparser.RobotFileParser()


def multi_get_robots_txt(urls, timeout=60):
    """Return a robotparser object for each url in the list"""

    with concurrent.futures.ProcessPoolExecutor() as executor:
        processes = executor.map(get_robots_txt, urls, timeout=timeout)

        for process in processes:
            yield process
