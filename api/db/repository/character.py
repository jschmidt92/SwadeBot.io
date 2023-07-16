from sqlalchemy.orm import Session
from typing import List, Optional

from db.models.association import gear_character, weapon_character
from db.models.character import Character
from db.models.user import User
from db.repository.encounter import retrieve_encounter
from db.repository.gear import retrieve_gear
from db.repository.power import retrieve_power
from db.repository.weapon import retrieve_weapon
from schemas.character import CharacterCreate, UpdateCharacter


class CharacterNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


def _get_character_by_id(id: int, db: Session) -> Character:
    character = db.query(Character).filter(Character.id == id).first()
    if character is None:
        raise CharacterNotFoundError(f"Character with id {id} not found")
    return character


def _get_user_by_id(id: int, db: Session) -> User:
    user = db.query(User).filter(User.discord_id == id).first()
    if user is None:
        raise UserNotFoundError(f"User with id {id} not found")
    return user


def _get_character_by_name(name: str, db: Session) -> Character:
    character = db.query(Character).filter(Character.character_name == name).first()
    if character is None:
        raise UserNotFoundError(f"Character with name {name} not found")
    return character


def _update_dict_field(character_field: dict, update_field: dict):
    if character_field is not None and update_field is not None:
        character_field.update(update_field)


def create_new_character(character: CharacterCreate, db: Session) -> Character:
    character_orm = Character(
        user_id=character.user_id,
        character_name=character.character_name,
        race=character.race,
        gender=character.gender,
        pace=character.pace,
        charisma=character.charisma,
        parry=character.parry,
        toughness=character.toughness,
        attributes=character.attributes,
        skills=character.skills,
        gear=character.gear,
        hindrances=character.hindrances,
        edges=character.edges,
        powers=character.powers,
        weapons=character.weapons,
        damage=character.damage,
        ammo=character.ammo,
        money=character.money,
    )
    db.add(character_orm)
    db.commit()
    db.refresh(character_orm)

    user = _get_user_by_id(character.user_id, db)
    user.characters.append(character_orm)
    db.commit()

    return character_orm


def retrieve_character(id: int, db: Session) -> Optional[Character]:
    try:
        return _get_character_by_id(id, db)
    except CharacterNotFoundError:
        return None


def retrieve_user_character(id: int, name: str, db: Session) -> Optional[Character]:
    user = _get_user_by_id(id, db)
    character = _get_character_by_name(name, db)

    if character.user_id != user.discord_id:
        raise CharacterNotFoundError(
            f"Character with name {name} does not belong to user with id {id}"
        )

    return character


def list_characters(db: Session) -> List[Character]:
    rows = db.query(Character).all()
    return rows if rows else []


def list_user_characters(id: int, db: Session) -> List[Character]:
    user = _get_user_by_id(id, db)
    rows = db.query(Character).filter(Character.user_id == user.discord_id).all()
    return rows if rows else []


def update_character(
    character_id: int, character: UpdateCharacter, db: Session
) -> Character:
    row = _get_character_by_id(character_id, db)

    _update_dict_field(row.attributes, character.attributes)
    _update_dict_field(row.skills, character.skills)
    _update_dict_field(row.gear, character.gear)
    _update_dict_field(row.damage, character.damage)

    for var, value in character.dict(
        exclude={"attributes", "skills", "gear", "damage"}, exclude_unset=True
    ).items():
        setattr(row, var, value)

    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def delete_character(id: int, db: Session) -> Character:
    character = _get_character_by_id(id, db)
    db.delete(character)
    db.commit()
    return character


def add_gear_to_character(
    character_name: str, gear_name: str, amount: int, db: Session
) -> Character:
    character = _get_character_by_name(character_name, db)
    gear = retrieve_gear(gear_name, db)

    stmt = gear_character.insert().values(
        character_id=character.id, gear_id=gear.id, quantity=amount
    )
    db.execute(stmt)
    db.commit()
    db.commit()

    return character


def add_power_to_character(character_id: int, power_id: int, db: Session) -> Character:
    character = _get_character_by_id(character_id, db)
    power = retrieve_power(power_id, db)

    character.powers.append(power)
    db.commit()

    return character


def add_weapon_to_character(
    character_name: str, weapon_name: str, amount: int, db: Session
) -> Character:
    character = _get_character_by_name(character_name, db)
    weapon = retrieve_weapon(weapon_name, db)

    stmt = weapon_character.insert().values(
        character_id=character.id, weapon_id=weapon.id, quantity=amount
    )
    db.execute(stmt)
    db.commit()

    return character


def add_character_to_encounter(
    character_id: int, encounter_id: int, db: Session
) -> Character:
    character = _get_character_by_id(character_id, db)
    encounter = retrieve_encounter(encounter_id, db)

    character.encounters.append(encounter)
    db.commit()

    return character


def has_enough_money(
    user_id: int, character_name: str, amount: int, db: Session
) -> bool:
    character = retrieve_user_character(user_id, character_name, db)
    return character.money >= amount


def add_money_to_character(
    user_id: int, character_name: str, amount: int, db: Session
) -> Character:
    character = retrieve_user_character(user_id, character_name, db)

    character.money += amount
    db.commit()

    return character


def subtract_money_to_character(
    user_id: int, character_name: str, amount: int, db: Session
) -> Character:
    if not has_enough_money(user_id, character_name, amount, db):
        raise ValueError(f"Character {character_name} does not have enough money")

    character = retrieve_user_character(user_id, character_name, db)
    character.money -= amount
    db.commit()

    return character


def check_money_for_character(user_id: int, character_name: str, db: Session) -> int:
    character = retrieve_user_character(user_id, character_name, db)
    db.commit()

    return character.money
