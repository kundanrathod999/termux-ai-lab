import os
from dotenv import load_dotenv

# Force load .env
load_dotenv(override=True)

class Config:
    PROVIDER = os.getenv("AI_PROVIDER", "you").lower()
    MODEL = os.getenv("MODEL", "you-answer")
    YOU_API_KEY = os.getenv("YOU_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    
    def get_api_key(self, provider=None):
        p = (provider or self.PROVIDER).lower()
        if p == "you":
            return self.YOU_API_KEY
        if p == "gemini":
            return self.GEMINI_API_KEY
        return os.getenv(f"{p.upper()}_API_KEY", "")

config = Config()
