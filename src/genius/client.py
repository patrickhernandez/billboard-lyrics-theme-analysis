from bs4 import BeautifulSoup
import re
import requests
from src.config.settings import settings

class GeniusClient:
    """
    """

    def __init__(self):
        self.access_token = settings.genius_access_token

    def get_genius_urls(self, tracks, artists):
        all_urls = []
        search_url = 'https://api.genius.com/search'
        headers = {'Authorization': f'Bearer {self.access_token}'}

        for track, artist in zip(tracks, artists):
            params = {'q': f'{track} {artist}'}
            response = requests.get(search_url, headers=headers, params=params).json()
            hits = response['response']['hits']
            if len(hits) == 0:
                all_urls.append(None)
                continue
            name = hits[0]['result']['primary_artist']['name']
            url = hits[0]['result']['url']

            if artist == name:
                all_urls.append(url)
            elif any(a in url.lower() for a in artist.lower().split()):
                all_urls.append(url)
            else:
                all_urls.append(None)

        return all_urls

    def get_genius_lyrics(self, urls):
        all_lyrics = []

        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            divs = soup.find_all('div', class_=re.compile(r'^Lyrics__Container-sc'))
            text = ' '.join(div.get_text(separator=' ', strip=True) for div in divs)

            if ']' in text:
                lyrics = re.sub(r'\[[^]]+\]', '', text.split(']', 1)[1])
            else:
                lyrics = text.split('Lyrics', 1)[1]
            
            lyrics = re.sub(r'\s+', ' ', lyrics).strip()
            all_lyrics.append(lyrics)
        
        return all_lyrics