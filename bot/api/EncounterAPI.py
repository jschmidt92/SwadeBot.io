from dotenv import load_dotenv
import requests
import os

load_dotenv()

BASE_URL = str(os.environ["BASE_URL"])


def add_character_encounter(id: int, encounter_id: list[int]):
    return requests.post(
        f"{BASE_URL}/encounters/characters/{id}", json={"encounter_id": encounter_id}
    )


def add_monster_encounter(id: int, encounter_id: list[int]):
    return requests.post(
        f"{BASE_URL}/encounters/monsters/{id}", json={"encounter_id": encounter_id}
    )


def create_encounter(name: str, notes: str = ""):
    return requests.post(f"{BASE_URL}/encounters", json={"name": name, "notes": notes})


def delete_encounter(id: int):
    return requests.delete(f"{BASE_URL}/encounters/{id}")


def get_all_encounters():
    return requests.get(f"{BASE_URL}/encounters")


def get_encounter_characters(id: int):
    return requests.get(f"{BASE_URL}/encounters/{id}/characters")


def get_encounter_monsters(id: int):
    return requests.get(f"{BASE_URL}/encounters/{id}/monsters")


def remove_character_encounter(id: int, encounter_id: list[int]):
    return requests.delete(
        f"{BASE_URL}/encounters/characters/{id}", json={"encounter_id": encounter_id}
    )


def remove_monster_encounter(id: int, encounter_id: list[int]):
    return requests.delete(
        f"{BASE_URL}/encounters/monsters/{id}", json={"encounter_id": encounter_id}
    )


def update_encounter(id: int, name: str = None, notes: str = None):
    data = {}
    if name is not None:
        data["name"] = name
    if notes is not None:
        data["notes"] = notes
    return requests.put(f"{BASE_URL}/encounters/{id}", json=data)
