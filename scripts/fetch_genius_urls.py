import pandas as pd
import json
from src.genius.client import GeniusClient

genius = GeniusClient()

popular_songs = pd.read_parquet('data/raw/popular_songs.parquet')
tracks = popular_songs['trackTitle']
artists = popular_songs['primary_artist']
genius_urls = genius.get_genius_urls(tracks, artists)

popular_songs['url'] = genius_urls
popular_songs_with_urls = popular_songs.dropna().reset_index(drop=True)

popular_songs_with_urls.to_parquet('data/interim/_songs_with_urls.parquet')