import pandas as pd
from src.utils.cleaning import get_popular_songs

full_charts = pd.read_parquet('data/raw/full_charts.parquet')
popular_songs = get_popular_songs(full_charts)

popular_songs.to_parquet('data/interim/popular_songs.parquet')