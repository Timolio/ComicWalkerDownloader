import requests
import json
from typing import Dict, List
from bs4 import BeautifulSoup
from comicwalker_downloader.exceptions import ParsingError, EpisodeNotFoundError
from comicwalker_downloader.utils import USER_AGENT

class ComicParser:
    def __init__(self, url: str) -> None:
        self.url = url
        self.data: dict = {}
        self.ep: dict = {}
        self._parse_data()

    def get_work_title(self) -> str:
        return self.data['work']['title']

    def set_episode(self, ep_number: int = None) -> None:
        if ep_number is None:
            self.ep = self.data['episode']
            return

        self.ep = next(
            (ep for ep in self.data['firstEpisodes']['result'] if ep['internal']['episodeNo'] == ep_number and ep['isActive']), None
        )

        if self.ep is None:
            raise EpisodeNotFoundError(f"Episode {ep_number} not found or not available")

    def get_episode_list(self, only_active: bool = False) -> List[Dict]:
        ep_list = []
        for ep in self.data['firstEpisodes']['result']:
            if only_active and not ep['isActive']:
                continue

            ep_list.append({
                'number': ep['internal']['episodeNo'],
                'title': ep['title'],
                'is_active': ep['isActive'],
            })
        return ep_list

    def get_current_episode(self) -> dict:
        return {
            'number': self.data['episode']['internal']['episodeNo'],
            'title': self.data['episode']['title']
        }

    def _parse_data(self) -> None:
        try:
            response = requests.get(
                self.url,
                headers={'User-Agent': USER_AGENT}
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            raise ParsingError("Connection error. Please check your internet connection") from e
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise ParsingError("Page not found. Please check the URL") from e
            raise ParsingError(f"HTTP error {response.status_code}") from e
        except requests.exceptions.RequestException as e:
            raise ParsingError(f"Failed to fetch page: {e}") from e

        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find('script', {'id': '__NEXT_DATA__'})

            if not script_tag:
                raise ParsingError("ComicWalker data not found")

            json_data = json.loads(script_tag.string)

            queries = json_data.get('props', {}).get('pageProps', {}).get('dehydratedState', {}).get('queries', [])

            work_data = next(
                (q.get('state', {}).get('data', {}) for q in queries
                 if isinstance(q.get('queryKey'), list) and q['queryKey'][0] == '/api/contents/details/work'),
                {}
            )
            episode_data = next(
                (q.get('state', {}).get('data', {}) for q in queries
                 if isinstance(q.get('queryKey'), list) and q['queryKey'][0] == '/api/contents/details/episode'),
                {}
            )

            work = work_data.get('work', {})
            first_episodes = work_data.get('firstEpisodes', {})
            episode = episode_data.get('episode', {})

            if not work or not first_episodes or not episode:
                raise ParsingError('Missing essential ComicWalker data')

            self.data = {'work': work, 'firstEpisodes': first_episodes, 'episode': episode}

        except json.JSONDecodeError as e:
            raise ParsingError("Failed to parse page data") from e
