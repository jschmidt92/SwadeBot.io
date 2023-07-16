from dotenv import load_dotenv
import requests
import os

load_dotenv()

BASE_URL = str(os.environ["BASE_URL"])


def buy_gear(user_id: int, character_name: str, gear_name: str, amount: int):
    return requests.put(
        f"{BASE_URL}/store/character/buy_gear",
        json={
            "user_id": user_id,
            "character_name": character_name,
            "gear_name": gear_name,
            "amount": amount,
        },
    )


def buy_weapon(user_id: int, character_name: str, weapon_name: str, amount: int):
    return requests.put(
        f"{BASE_URL}/store/character/buy_weapon",
        json={
            "user_id": user_id,
            "character_name": character_name,
            "weapon_name": weapon_name,
            "amount": amount,
        },
    )


def check_money(user_id: int, character_name: str):
    return requests.put(
        f"{BASE_URL}/characters/check_money",
        json={"user_id": user_id, "character_name": character_name},
    )


def list_gear():
    return requests.get(f"{BASE_URL}/store/gear")


def list_weapons():
    return requests.get(f"{BASE_URL}/store/weapons")
