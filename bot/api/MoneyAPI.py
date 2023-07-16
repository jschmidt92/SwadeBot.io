from dotenv import load_dotenv
import requests
import os

load_dotenv()

BASE_URL = str(os.environ["BASE_URL"])


def add_money(user_id: int, character_name: str, amount: int):
    return requests.post(
        f"{BASE_URL}/characters/add_money",
        json={
            "user_id": user_id,
            "character_name": character_name,
            "amount": amount,
        },
    )


def check_money(user_id: int, character_name: str):
    return requests.get(
        f"{BASE_URL}/characters/check_money",
        params={"user_id": user_id, "character_name": character_name},
    )


def subtract_money(user_id: int, character_name: str, amount: int):
    return requests.post(
        f"{BASE_URL}/characters/subtract_money",
        json={
            "user_id": user_id,
            "character_name": character_name,
            "amount": amount,
        },
    )
