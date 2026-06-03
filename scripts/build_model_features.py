import pandas as pd

popular_songs = pd.read_parquet('data/interim/popular_songs_with_lyrics.parquet')
themes = pd.read_parquet('data/interim/theme_scores.parquet')
embeddings = pd.read_parquet('data/interim/embeddings_pca.parquet')

complete_df = pd.concat([popular_songs, themes, embeddings], axis=1)
complete_df = complete_df.drop(columns=['artists', 'url', 'lyrics'])
complete_df.to_parquet('data/processed/songs_with_themes_embeddings.parquet')