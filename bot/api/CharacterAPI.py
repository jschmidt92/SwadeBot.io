from dotenv import load_dotenv
import requests
import os

load_dotenv()

BASE_URL = str(os.environ["BASE_URL"])


def get_all_characters():
    return requests.get(
        f"{BASE_URL}/characters",
        json={},
    )


def get_player_character(user_id: int, character_name: str):
    return requests.get(f"{BASE_URL}/users/{user_id}/characters/{character_name}")


def get_player_characters(user_id: int):
    return requests.get(f"{BASE_URL}/users/{user_id}/characters")
