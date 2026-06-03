import pandas as pd
import numpy as np
import torch
from tqdm import tqdm
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer
from src.config.settings import settings

def get_device_batch():
    if torch.cuda.is_available():
        device = 'cuda'
        batch_size = 16
    elif torch.backends.mps.is_available():
        device = 'mps'
        batch_size = 8
    else:
        device = 'cpu'
        batch_size = 4
    
    return device, batch_size

def get_song_embeddings(lyrics):
    device, batch_size = get_device_batch()

    model = SentenceTransformer('microsoft/harrier-oss-v1-0.6b', device=device, token=settings.hf_access_token)
    lyrics = list(lyrics)

    instruction = ('Instruct: Represent the song lyrics for thematic similarity genre clustering, and lyrical semantic analysis.')

    embeddings = []

    for i in tqdm(range(0, len(lyrics), batch_size)):
        batch = lyrics[i:i + batch_size]
        batch = [instruction + song for song in batch]

        batch_emb = model.encode(batch, normalize_embeddings=True)
        embeddings.extend(batch_emb.tolist())

    return pd.DataFrame({'embedding': embeddings})

df = pd.read_parquet('data/interim/songs_with_lyrics.parquet')
embeddings = get_song_embeddings(df['lyrics'])

embeddings.to_parquet('data/raw/embeddings.parquet')

X = np.vstack(embeddings['embedding'].values)
pca = PCA(n_components=2)
components = pca.fit_transform(X)
pca_df = pd.DataFrame({'pca_1': components[:, 0], 'pca_2': components[:, 1],})

pca_df.to_parquet('data/interim/embeddings_pca.parquet')