from sqlalchemy.orm import Session

from db.models.character import Character
from db.models.encounter import Encounter
from db.models.gear import Gear
from db.models.monster import Monster
from db.models.power import Power
from db.models.user import User
from db.models.weapon import Weapon


class CharacterNotFoundError(Exception):
    pass


class EncounterNotFoundError(Exception):
    pass


class GearNotFoundError(Exception):
    pass


class MonsterNotFoundError(Exception):
    pass


class PowerNotFoundError(Exception):
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


def _get_encounter_by_id(encounter_id: int, db: Session) -> Encounter:
    encounter = db.query(Encounter).filter(Encounter.id == encounter_id).first()
    if encounter is None:
        raise EncounterNotFoundError(f"Encounter with id {encounter_id} not found")
    return encounter


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


def _get_monster_by_id(id: int, db: Session) -> Monster:
    monster = db.query(Monster).filter(Monster.id == id).first()
    if monster is None:
        raise MonsterNotFoundError(f"Monster with id {id} not found")
    return monster


def _get_monster_by_name(name: str, db: Session) -> Monster:
    monster = db.query(Monster).filter(Monster.monster_name == name).first()
    if monster is None:
        raise UserNotFoundError(f"Monster with name {name} not found")
    return monster


def _get_power_by_id(power_id: int, db: Session) -> Power:
    power = db.query(Power).filter(Power.id == power_id).first()
    if power is None:
        raise PowerNotFoundError(f"Power with id {power_id} not found")
    return power


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


def _update_character_dict_field(character_field: dict, update_field: dict):
    if character_field is not None and update_field is not None:
        character_field.update(update_field)


def _update_monster_dict_field(monster_field: dict, update_field: dict):
    if monster_field is not None and update_field is not None:
        monster_field.update(update_field)


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


def _get_weapon_by_id(weapon_id: int, db: Session) -> Weapon:
    weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
    if weapon is None:
        raise WeaponNotFoundError(f"Weapon with id {weapon_id} not found")
    return weapon


def _get_weapon_by_name(weapon_name: int, db: Session) -> Weapon:
    weapon = db.query(Weapon).filter(Weapon.name == weapon_name).first()
    if weapon is None:
        raise WeaponNotFoundError(f"Weapon with name {weapon_name} not found")
    return weapon
