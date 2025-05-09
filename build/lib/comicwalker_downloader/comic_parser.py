import requests
import json
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
    
    def get_cli_list(self) -> list:
        cli_list = []
        for ep in self.data['firstEpisodes']['result']:
            if not ep['isActive']:
                continue
            item = f'( {ep['internal']['episodeNo']} )   {ep['title']}' + ('   <-- CURRENT' if ep['internal']['episodeNo'] == self.data['episode']['internal']['episodeNo'] else '')
            cli_list.append(item)
        
        return cli_list

    def _parse_data(self) -> None:
            try:
                response = requests.get(self.url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
                })
                response.raise_for_status()
                html_content = response.text

                soup = BeautifulSoup(html_content, 'html.parser')

                script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
                if not script_tag:
                    raise ValueError("JSON script tag not found")

                json_data = json.loads(script_tag.string)
                work = json_data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['work']
                first_episodes = json_data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['firstEpisodes']
                episode = json_data['props']['pageProps']['dehydratedState']['queries'][2]['state']['data']['episode']

                self.data = {'work': work, 'firstEpisodes': first_episodes, 'episode': episode}
            except Exception as e:
                raise e
