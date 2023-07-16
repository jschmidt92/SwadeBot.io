from dotenv import load_dotenv
from pathlib import Path
from urllib import parse

import os

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "SwadeBot.io"
    PROJECT_VERSION: str = "1.0.0"
    TOKEN: str = ""
    CLIENT_ID: str = ""
    CLIENT_SECRET: str = ""
    REDIRECT_URI: str = "http://example.com/api/oauth/callback"
    OAUTH_URL: str = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={parse.quote(REDIRECT_URI)}&response_type=code&scope=identify"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "verysecret")


settings = Settings()
