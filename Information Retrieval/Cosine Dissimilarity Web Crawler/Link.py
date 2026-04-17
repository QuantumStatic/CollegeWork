"""This file contains the link class. Every link is generally stored as a link object"""
from __future__ import annotations
import validators
import bs4
import requests
import tldextract
import urllib.parse
from sortedcontainers import SortedList
import re
import random


class Link:

    # class objects that help us with processing
    _extractor = tldextract.TLDExtract()
    _domain_count: dict[str, tuple[int, float]] = {}
    _per_page_links: SortedList[int] = SortedList()
    _pages_found: int = 0
    _total_domains = 0
    _non_webpage_pattern = re.compile(r'.*\.(jpg|jpeg|png|gif|bmp|ico|svg|tif|tiff|bpg|img|pdf|docx?|xlsx?|pptx?|txt|rtf|csv)$')

    # Using slots to reduce memory consumption per object
    __slots__ = ["_link", "_domain_name", "_response", "_language", "_links_in_this_page", "_title", "title_encoding", "age", "num_links"]
    
    def __init__(self, link, response=None, language=None):
        """Initialising the object and processing response if we get one"""
        self._link: str = link
        self._domain_name = Link._get_domain_name(link)
        self._response: requests.Response = response
        self._language: str = language
        self._links_in_this_page = []
        self._title = "-2"
        self.age = 0
        self.title_encoding = None
        self.num_links = 0

        self._process_response()

    def _process_response(self):
        """Internal function to extract links in current page's response and find headings for dissimilarity"""
        if self._response is not None:
            # Create Beautiful Soup object
            soup = bs4.BeautifulSoup(self._response.text, "html.parser")
            for link in soup.find_all("a"):
                if link.has_attr("href"):
                    self._links_in_this_page.append(link["href"])
            
            # Clean and validate links and put them in a set to remove duplicates
            self._links_in_this_page = tuple(set(filter(Link.validate_url, map(self._clean_url, self._links_in_this_page))))
            self.num_links = len(self._links_in_this_page)

            Link._per_page_links.add(self.num_links)
            Link._pages_found += 1

            # add to speed up
            if Link._pages_found > 2500:
                Link._per_page_links = set(random.sample(sorted(Link._per_page_links), k = 1200))
                Link._pages_found = 1200
            
            # Additional processing required for the machine learning model
            self._title = ""
            try:
                for heading in soup.find_all(["h1", "h2"]):
                    try:
                        self._title += heading.text.strip()
                    except Exception:
                        self._title += '-1'
                        print('f')
            except Exception as e:
                self._title = None
                print("set to None", e)

        self._response = None

    def add_language(self, language):
        self._language: str = language

    def add_response(self, response: requests.Response):
        if self._response is not None:
            raise Exception("Link already has a response")
        self._response = response
        self._process_response()

    def increment_age(self):
        self.age += 1

    @property
    def link(self) -> str:
        return self._link

    @property
    def language(self) -> str:
        return self._language

    @property
    def response(self) -> requests.Response:
        return self._response

    @property
    def domain_name(self) -> str:
        return self._domain_name

    @property
    def links_in_this_page(self) -> list:
        return self._links_in_this_page
    
    @property
    def title(self) -> str:
        return self._title
    
    @classmethod
    def _extract_domain_name(cls, link: str) -> str:
        """Returns the fully qualified domain name"""
        return cls._extractor.extract_urllib(urllib.parse.urlsplit(link)).fqdn

    @classmethod
    def _get_domain_name(cls, link: str) -> str:  
        return cls._extract_domain_name(link)
    
    def increase_domain_count(self):
        try:
            Link._domain_count[self._domain_name] = (Link._domain_count[self._domain_name][0] + 1, Link._domain_count[self._domain_name][1])
        except KeyError:
            Link._domain_count[self._domain_name] = (1, 0)
    
    @classmethod
    def re_eval_domain_score(cls) -> float:
        """Function create domain distribution. It usees a sorted container with O(logn) insert and find"""
        link_vals =  SortedList(sorted((x[0] for x in cls._domain_count.values())))
        cls._total_domains = len(cls._domain_count)

        for  domain_name, domain_count in cls._domain_count.items():
            # It would originally return percentile but we modified to account for duplicates
            cls._domain_count[domain_name] = (domain_count[0], ((link_vals.bisect_left(domain_count[0]) + link_vals.bisect_right(domain_count[0])) // 2) / cls._total_domains)
            
            #use this instead all other calculations to speed up
            # cls._domain_count[domain_name] = (domain_count[0], (domain_count[0] / 50))

    @classmethod
    def get_domain_score(cls, link:str) -> float:
        return cls._domain_count.setdefault(cls._extract_domain_name(link), (0, 0))[1]
    
    @classmethod
    def get_domain_count(cls, link:str) -> int:
        return cls._domain_count.setdefault(cls._extract_domain_name(link), (0, 0))[0]

    def __str__(self) -> str:
        return f"Link(domain_name={self._domain_name}, language={self._language}, links={len(self._links_in_this_page)})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    @classmethod
    def get_percentile_of_links(cls, links_in_page:int)->float:
        # Similar to domain count we reutrn our modified percentile of links
        return ((cls._per_page_links.bisect_left(links_in_page) + cls._per_page_links.bisect_right(links_in_page)) // 2) / cls._pages_found
    
    def _clean_url(self, url:str) -> str:
        return Link.clean_url(url, self)

    @staticmethod
    def clean_url(url:str, domain_link_obj:Link = None) -> str:
        
        # Remove white spaces
        url = url.strip()

        # check if a relative link
        if domain_link_obj is not None and url.startswith('/'):
            url = domain_link_obj.complete_relative_url(url)
        
        parts = urllib.parse.urlparse(url)
        
        # Remove fragment and check if query is empty or starts with '?'
        query = '' if not parts.query or parts.query.startswith('?') else parts.query
        
        # Remove unnecessary slashes from the path
        path = '/'.join(filter(bool, parts.path.split('/')))
        cleaned_parts = parts._replace(fragment="", query=query, path=path)
        
        new_query = Link._remove_url_trackers(cleaned_parts)
        cleaned_parts = cleaned_parts._replace(query=new_query)
        
        cleaned_url = urllib.parse.urlunparse(cleaned_parts)
        return cleaned_url

    @classmethod
    def validate_url(cls, url:str) -> bool:
        try:
            validators.url(url)
        except Exception:
            return False
        else:
            return not bool(cls._non_webpage_pattern.search(url))

    @staticmethod
    def _remove_url_trackers(url_components:urllib.parse.ParseResult) -> urllib.parse.ParseResult:
        """Remove trackers from the url"""
        query_dict = urllib.parse.parse_qs(url_components.query)

        # Remove the tracking parameters you know about
        # You can add more parameters to this list
        tracking_parameters = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
                            'ref_', 'pd_rd_w', 'pd_rd_wg', 'pd_rd_r', 'pf_rd_p', 'pf_rd_r']

        for param in tracking_parameters:
            query_dict.pop(param, None)

        return urllib.parse.urlencode(query_dict, doseq=True)


    def complete_relative_url(self, url:str) -> str:
        return urllib.parse.urljoin(self._link, url)

