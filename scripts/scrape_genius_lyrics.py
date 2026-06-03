import pandas as pd
import json
from src.genius.client import GeniusClient

genius = GeniusClient()

popular_songs_with_urls = pd.read_parquet('data/interim/songs_with_urls.parquet')
genius_urls = popular_songs_with_urls['url']
genius_lyrics = genius.get_genius_lyrics(genius_urls)

popular_songs_with_urls['lyrics'] = genius_lyrics
popular_songs_with_urls['characters'] = [len(song) for song in popular_songs_with_urls['lyrics']]
popular_songs_with_urls['words'] = [len(song.split()) for song in popular_songs_with_urls['lyrics']]

popular_songs_with_lyrics = popular_songs_with_urls[
    (popular_songs_with_urls['characters'] >= 600)
    & (popular_songs_with_urls['characters'] <= 5000)
    & (popular_songs_with_urls['words'] >= 150)]
popular_songs_with_lyrics = popular_songs_with_lyrics[popular_songs_with_lyrics['rank'] <= 50]
popular_songs_with_lyrics = popular_songs_with_lyrics.drop(columns=['characters', 'words']).reset_index(drop=True)

popular_songs_with_lyrics.to_parquet('data/interim/songs_with_lyrics.parquet')