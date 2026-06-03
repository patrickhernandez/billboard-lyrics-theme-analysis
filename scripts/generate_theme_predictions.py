from __future__ import annotations

import pandas as pd
import asyncio
from typing import Literal, get_args
from chatlas import ChatOpenAI, parallel_chat_structured
from pydantic import BaseModel, Field
from src.config.settings import settings

ThemeName = Literal[
    'Love/Romance',
    'Heartbreak/Loss',
    'Party/Celebration',
    'Empowerment/Confidence',
    'Ambition/Success',
    'Mental Health/Inner Struggle',
    'Nostalgia/Reflection',
    'Social Commentary',
    'Sexual Desire',
    'Resilience/Survival',
]

class ThemePrediction(BaseModel):
    theme: ThemeName
    confidence: float = Field(ge=0.0, le=1.0)


class ThemeOutput(BaseModel):
    themes: list[ThemePrediction] = Field(min_length=3, max_length=3)


fallback_value = {
    'themes': [
        {
            'theme': 'Love/Romance',
            'confidence': 0.0,
        },
        {
            'theme': "Heartbreak/Loss",
            'confidence': 0.0,
        },
        {
            'theme': 'Party/Celebration',
            'confidence': 0.0,
        },
    ]
}

df = pd.read_parquet('data/interim/songs_with_lyrics.parquet')

with open('prompts/theme_classification_prompt.md', 'r', encoding='utf-8') as f:
    system_prompt = f.read()

chat = ChatOpenAI(
    model='gpt-5-mini',
    api_key=settings.openai_api_key,
    system_prompt=system_prompt,
)

predictions = asyncio.run(
    parallel_chat_structured(
        chat,
        prompts=df['lyrics'].astype(str).tolist(),
        data_model=ThemeOutput,
        on_error='continue',
    )
)

results = []

for result in predictions:
    if result is None or isinstance(result, Exception):
        results.append(fallback_value.copy())
        continue

    results.append(result.data.model_dump())

all_themes = list(get_args(ThemeName))

theme_rows = []

for song_output in results:
    scores = {theme: 0.0 for theme in all_themes}

    for item in song_output.get('themes', []):
        scores[item['theme']] = item['confidence']

    theme_rows.append(scores)

theme_df = pd.DataFrame(theme_rows)
theme_df['primary_theme'] = theme_df.idxmax(axis=1)
theme_df.to_parquet('data/interim/theme_scores.parquet')