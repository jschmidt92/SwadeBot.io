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


class CharacterNotFoundError(Exception):
    pass


class GearNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class WeaponNotFoundError(Exception):
    pass


def _get_character_by_id(id: int, db: Session) -> Character:
    character = db.query(Character).filter(Character.id == id).first()
    if character is None:
        raise CharacterNotFoundError(f"Character with id {id} not found")
    return character


def _get_character_by_name(name: str, db: Session) -> Character:
    character = db.query(Character).filter(Character.character_name == name).first()
    if character is None:
        raise UserNotFoundError(f"Character with name {name} not found")
    return character


def _get_gear_by_id(gear_id: int, db: Session) -> Gear:
    gear = db.query(Gear).filter(Gear.id == gear_id).first()
    if gear is None:
        raise GearNotFoundError(f"Gear with id {gear_id} not found")
    return gear


def _get_gear_by_name(gear_name: int, db: Session) -> Gear:
    gear = db.query(Gear).filter(Gear.name == gear_name).first()
    if gear is None:
        raise GearNotFoundError(f"Gear with name {gear_name} not found")
    return gear


def _get_weapon_by_name(weapon_name: int, db: Session) -> Weapon:
    weapon = db.query(Weapon).filter(Weapon.name == weapon_name).first()
    if weapon is None:
        raise WeaponNotFoundError(f"Weapon with name {weapon_name} not found")
    return weapon


def _get_user_by_id(id: int, db: Session) -> User:
    user = db.query(User).filter(User.discord_id == id).first()
    if user is None:
        raise UserNotFoundError(f"User with id {id} not found")
    return user


def _get_weapon_by_id(weapon_id: int, db: Session) -> Weapon:
    weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
    if weapon is None:
        raise WeaponNotFoundError(f"Weapon with id {weapon_id} not found")
    return weapon


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
