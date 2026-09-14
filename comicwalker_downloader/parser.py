import json
import requests
from bs4 import BeautifulSoup
from comicwalker_downloader.api import TIMEOUT, make_session
from comicwalker_downloader.exceptions import InvalidURLError, NetworkError, ParsingError
from comicwalker_downloader.models import Work

WORK_QUERY_KEY = '/api/contents/details/work'
EPISODE_QUERY_KEY = '/api/contents/details/episode'


def fetch_work(url: str, session: requests.Session | None = None) -> Work:
    own_session = None
    if session is None:
        own_session = make_session()
        session = own_session

    try:
        response = session.get(url, timeout=TIMEOUT)
        response.raise_for_status()
        html = response.text
    except requests.exceptions.Timeout as e:
        raise NetworkError("Request timed out. The site is not responding") from e
    except requests.exceptions.ConnectionError as e:
        raise NetworkError("Connection error. Please check your internet connection") from e
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else '?'
        if status == 404:
            raise InvalidURLError("Page not found. Please check the URL") from e
        raise NetworkError(f"HTTP error {status}") from e
    except requests.exceptions.RequestException as e:
        raise NetworkError(f"Failed to fetch page: {e}") from e
    finally:
        if own_session is not None:
            own_session.close()

    return parse_work(html)


def parse_work(html: str) -> Work:
    soup = BeautifulSoup(html, 'html.parser')
    script_tag = soup.find('script', {'id': '__NEXT_DATA__'})

    if not script_tag:
        raise ParsingError("ComicWalker data not found")

    try:
        payload = json.loads(script_tag.get_text())
    except json.JSONDecodeError as e:
        raise ParsingError("Failed to parse page data") from e

    props = payload.get('props') or {}
    page_props = props.get('pageProps') or {}
    dehydrated = page_props.get('dehydratedState') or {}
    queries = dehydrated.get('queries') or []

    work = Work.from_api(
        find_query_data(queries, WORK_QUERY_KEY),
        find_query_data(queries, EPISODE_QUERY_KEY),
    )

    if not work.title or not work.episodes or work.current_episode is None:
        raise ParsingError('Missing essential ComicWalker data')

    return work


def find_query_data(queries: list, wanted_key: str) -> dict:
    for query in queries:
        if not isinstance(query, dict):
            continue
        query_key = query.get('queryKey')
        if isinstance(query_key, list) and query_key and query_key[0] == wanted_key:
            state = query.get('state') or {}
            return state.get('data') or {}
    return {}
