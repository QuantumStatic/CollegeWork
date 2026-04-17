"""
This file contains the code to scrape google search results
"""


import bs4 as bs

import requests
import urllib.parse

# from myfunctions import execute_this


def get_raw_query_results(query: str, page: int = 1) -> str:
    """
    This function returns the raw html of the google search results
    """

    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}" + (
        f"&start={10*(page-1)}" if page > 1 else ""
    )

    response = requests.get(url, timeout=10)

    return response


def get_result_list(response) -> list:
    """
    This function returns the list of results after parsing the response
    """

    # parse the response
    soup = bs.BeautifulSoup(response.text, "html.parser")

    # There is a div with id="main" which contains all the results
    main_stuff = soup.find("div", id="main")

    # The search is in div tags and the first two children of the div are not results
    results = tuple(filter(lambda x: x.name == "div", main_stuff.children))[2:]

    # The results are in div tags and the first child of the div is the result
    results = map(lambda x: tuple(x.children)[0], results)

    # The results also contain other google search results and they generally have other than 2 children
    results = filter(lambda x: len(tuple(x.children)) == 2, results)

    # The first child contains the link to the result
    results = tuple(map(lambda x: tuple(x.children)[0], results))

    # print(results[0].prettify())
    # print(results[0].prettify())

    # The link is in the href attribute of the a tag with some google stuff in the beginning
    final_results = []
    for result in results:
        if result.name == "a":
            final_results.append(result["href"][7:])
        else:
            final_results.extend(map(lambda y: y['href'][7:], filter(lambda x: x.name=='a', result.descendants)))

    return tuple(final_results)


def render_request(raw_response):
    soup = bs.BeautifulSoup(raw_response.text, "html.parser")
    with open(
        r"/Users/utkarsh/Desktop/Utkarsh/NYU/Year 1/Semester 1/Web Search Engines/Assignments/HW 1.html",
        "wb",
    ) as f:
        f.write(soup.prettify("utf-8"))


def get_google_search_results(query: str, page: int = 1) -> list:
    raw_response = get_raw_query_results(query, page)
    result_list = get_result_list(raw_response)
    return clean_links(result_list)

def clean_links(links: list[str]) -> list:
    cleaned_links = []
    for link in links:
        parsed_url = urllib.parse.urlsplit(link)
        if parsed_url.scheme[:4] != 'http':
            continue
        split_link = link.split('&')
        split_link = list(filter(lambda x: (not x.startswith("usg=")) and (not x.startswith("ved=")) and (not x.startswith("sa=")), split_link))
        cleaned_links.append('&'.join(split_link))

    return cleaned_links

# @execute_this
def testing_google_resutls_scraping():
    raw_response = get_raw_query_results("Hello")
    # render_request(raw_response)
    results = get_result_list(raw_response)
    results = clean_links(results)
    print(get_google_search_results("Hello"))
