import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    genius_access_token = os.getenv('GENIUS_ACCESS_TOKEN')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    hf_access_token = os.getenv('HF_ACCESS_TOKEN')

settings = Settings()