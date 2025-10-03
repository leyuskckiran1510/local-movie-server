from typing import Literal, NamedTuple
from urllib.parse import urlencode
from urllib.request import urlopen

Result_t = Literal[
    'tv', 'movie', 'people', 'keyword', 'collection', 'companies', 'network', 'award'
]


class Movie_t(NamedTuple):
    name: str
    id: str
    desc: str
    date: str
    img: str
    result_type: Result_t


class TMDB:
    __base_url = 'https://www.themoviedb.org/search'

    def __init__(self):
        pass

    def prep_url(self, search: str):
        return self.__base_url + '?' + urlencode({'query': search.strip()})

    def fetch_url(self, url: str):
        response = urlopen(url)
        html = response.read().decode('utf-8')
        return html

    def parse_results(self, html: str) -> list[Movie_t]:
        return []

    def search(self, query: str):
        url = self.prep_url(query)
        html = self.fetch_url(url)
        _ = self.parse_results(html)
