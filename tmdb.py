import json
import os
from typing import Any, Literal, Required, TypedDict
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from utils import load_env

load_env()

Language_t = Literal['en-US']
BASE_URL = 'https://api.themoviedb.org/3/search/'

TV_URL = BASE_URL + 'tv'
MV_URL = BASE_URL + 'movie'


class SearchQuery(TypedDict, total=False):
    query: Required[str]
    include_adult: bool
    language: Language_t
    page: int
    year: str


class SearchQMovie(SearchQuery, total=False):
    # only in movies
    primary_release_year: str
    region: str


class SearchQTV(SearchQuery, total=False):
    # only on tvs
    first_air_date_year: int  # 1000..9999


class SearchResult(TypedDict):
    adult: bool
    backdrop_path: str
    genre_ids: list[int]
    id: int
    original_language: str
    overview: str
    popularity: float
    poster_path: str

    vote_average: float
    vote_count: int


class SearchResultTv(SearchResult, total=False):
    # only on tvs
    origin_country: list[str]
    original_name: str
    name: str
    first_air_date: str


class SearchResultMovie(SearchResult, total=False):
    # only on movies
    original_title: str
    release_date: str
    title: str
    video: bool


class SearchResponse(TypedDict):
    page: int
    results: list[SearchResultTv | SearchResultMovie]
    total_pages: int
    total_results: int


class SimplifiedResult(SearchResult):
    name: str
    original_name: str
    release_date: str
    search_type: Literal['tv', 'movie']


class SimpleSearchResponse(TypedDict):
    page: int
    results: list[SimplifiedResult]
    total_pages: int
    total_results: int


class Search:
    headers = {
        'accept': 'application/json',
    }

    def __init__(self, *, tmdb_api: str | None = None):
        api_key = tmdb_api or os.environ.get('TMDB_API')
        if not api_key:
            raise ValueError(
                'Api key not provided. Visit https://www.themoviedb.org/settings/api .\n'
                '\t1) Navigate to API Read Access Token'
                '\t2) Copy the token'
            )
        self.headers.update({'Authorization': f'Bearer  {api_key}'})

    def fetch(self, url: str) -> str:
        req = Request(url, headers=self.headers)
        with urlopen(req) as response:
            response = response.read().decode('utf-8')
        return response

    def simplify_response(
        self, res: Any, is_movie: bool = True
    ) -> SimpleSearchResponse:
        ss = SimpleSearchResponse(res)
        results = ss['results']
        results_new: list[SimplifiedResult] = []
        for item in results:
            name = item.get('name') or item.get('title', '')

            original_name = item.get('original_name') or item.get('original_title', '')
            release_date = item.get('first_air_date') or item.get('release_date', '')
            results_new.append(
                {
                    **item,
                    'name': name,
                    'original_name': original_name,
                    'release_date': release_date,
                    'search_type': 'movie' if is_movie else 'tv',
                }
            )
        ss['results'] = results_new
        return ss

    def search_movie(self, query: SearchQMovie) -> SimpleSearchResponse:
        url = MV_URL + '?' + urlencode(query=query)
        dit = json.loads(self.fetch(url))
        res = SearchResponse(dit)
        return self.simplify_response(res)

    def search_tv(self, query: SearchQTV) -> SimpleSearchResponse:
        url = TV_URL + '?' + urlencode(query=query)
        dit = json.loads(self.fetch(url))
        res = SearchResponse(dit)
        return self.simplify_response(res, is_movie=False)

    def search(self, query: SearchQuery) -> SimpleSearchResponse:
        mvs = self.search_movie(SearchQMovie(**query))
        tvs = self.search_tv(SearchQTV(**query))
        alls: SimpleSearchResponse = {
            'page': mvs['page'],
            'total_pages': mvs['total_pages'] + tvs['total_pages'],
            'total_results': mvs['total_results'] + tvs['total_results'],
            'results': mvs['results'] + tvs['results'],
        }
        return alls


if __name__ == '__main__':
    s = Search()
    ha = s.search({'query': 'falling'})
    for item in ha['results']:
        print(item['name'], item['release_date'], item['id'], item['overview'][:10])
