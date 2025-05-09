import requests
import json
from typing import Dict, List
from bs4 import BeautifulSoup
from loguru import logger

class ComicParser:
    def __init__(self, url: str) -> None:
        self.url = url
        self.data: dict = {}
        self.ep: dict = {}
        self._parse_data()

    def set_episode(self, ep_number: int = None) -> None:
        if ep_number is None:
            self.ep = self.data['episode']
            return

        self.ep = next((ep for ep in self.data['firstEpisodes']['result'] if ep['internal']['episodeNo'] == ep_number), None)
    
    def get_episode_list(self, only_active: bool = False) -> List[Dict]:
        ep_list = []
        for ep in self.data['firstEpisodes']['result']:
            if only_active and not ep['isActive']:
                continue

            # item = f'( {ep['internal']['episodeNo']} )   {ep['title']}' + ('   <-- CURRENT' if ep['internal']['episodeNo'] == self.data['episode']['internal']['episodeNo'] else '')

            ep_list.append({
                'number': ep['internal']['episodeNo'],
                'title': ep['title'],
                'is_active: ': ep['isActive'],
            })
        return ep_list
    
    def get_current_episode(self) -> list:
        return {
            'number': self.data['episode']['internal']['episodeNo'],
            'title': self.data['episode']['title']
        }

    def _parse_data(self) -> None:
        try:
            response = requests.get(
                self.url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
                }
            )
            response.raise_for_status()
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
            if not script_tag:
                raise ValueError("ComicWalker __NEXT_DATA__ script tag not found")
            json_data = json.loads(script_tag.string)
            work = json_data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['work']
            first_episodes = json_data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['firstEpisodes']
            episode = json_data['props']['pageProps']['dehydratedState']['queries'][2]['state']['data']['episode']
            if not work or not first_episodes or not episode:
                raise ValueError('Misssing essential ComicWalker data for parsing')
            self.data = {'work': work, 'firstEpisodes': first_episodes, 'episode': episode}
        except Exception as e:
            raise ValueError(f"Failed to parse ComicWalker data: {e}")
