from sqlalchemy.orm import Session
from typing import Any, Dict, List

from db.models.character import Character
from db.models.gear import Gear
from db.models.user import User
from db.models.weapon import Weapon
from db.repository.character import (
    add_gear_to_character,
    add_weapon_to_character,
)
from db.repository.utilities import (
    _get_user_by_id,
    _get_character_by_id,
    _get_character_by_name,
    _get_gear_by_id,
    _get_gear_by_name,
    _get_weapon_by_id,
    _get_weapon_by_name,
    CharacterNotFoundError,
    GearNotFoundError,
    WeaponNotFoundError,
)


def buy_weapon(
    user_id: int, character_name: str, weapon_name: str, amount: int, db: Session
) -> Character:
    user = _get_user_by_id(user_id, db)
    character = _get_character_by_name(character_name, db)
    weapon = _get_weapon_by_name(weapon_name, db)

    if character.money < weapon.cost * amount:
        raise Exception(
            f"The character does not have enough money to buy the {weapon.name}"
        )

    character.money -= weapon.cost * amount
    add_weapon_to_character(character_name, weapon_name, amount, db=db)
    db.commit()
    return character


def list_weapons(db: Session) -> List[Weapon]:
    rows = db.query(Weapon).all()
    weapons = []
    if rows:
        for row in rows:
            weapon_dict = row.__dict__
            weapon_dict.pop("_sa_instance_state", None)
            weapons.append(weapon_dict)
    return weapons


def sell_weapon(character_id: int, weapon_id: int, db: Session) -> Character:
    character = _get_character_by_id(character_id, db)
    weapon = _get_weapon_by_id(weapon_id, db)

    if character is None:
        raise CharacterNotFoundError(f"Character with id {id} not found")

    if weapon not in character.weapons:
        raise WeaponNotFoundError(f"The character does not own the {weapon.name}")

    character.weapons.remove(weapon)
    character.money += weapon.cost * 0.35
    db.commit()
    return character


def list_gear(db: Session) -> List[Gear]:
    rows = db.query(Gear).all()
    gear = []
    if rows:
        for row in rows:
            gear_dict = row.__dict__
            gear_dict.pop("_sa_instance_state", None)
            gear.append(gear_dict)
    return gear


def buy_gear(
    user_id: int, character_name: str, gear_name: str, amount: int, db: Session
) -> Character:
    user = _get_user_by_id(user_id, db)
    character = _get_character_by_name(character_name, db)
    gear = _get_gear_by_name(gear_name, db)

    if character.money < gear.cost * amount:
        raise Exception(
            f"The character does not have enough money to buy the {gear.name}"
        )

    character.money -= gear.cost * amount
    add_gear_to_character(character_name, gear_name, amount, db=db)
    db.commit()
    return character


def sell_gear(character_id: int, gear_id: int, db: Session) -> Character:
    character = _get_character_by_id(character_id, db)
    gear = _get_gear_by_id(gear_id, db)

    if character is None:
        raise CharacterNotFoundError(f"Character with id {id} not found")

    if gear not in character.gear:
        raise GearNotFoundError(f"The character does not own the {gear.name}")

    character.gear.remove(gear)
    character.money += gear.cost * 0.35
    db.commit()
    return character
