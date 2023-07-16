from sqlalchemy.orm import Session
from typing import List, Optional

from db.models.association import gear_monster, weapon_monster
from db.models.monster import Monster
from db.models.user import User
from db.repository.encounter import retrieve_encounter
from db.repository.gear import retrieve_gear
from db.repository.power import retrieve_power
from db.repository.weapon import retrieve_weapon
from schemas.monster import MonsterCreate, UpdateMonster


class MonsterNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


def _get_monster_by_id(id: int, db: Session) -> Monster:
    monster = db.query(Monster).filter(Monster.id == id).first()
    if monster is None:
        raise MonsterNotFoundError(f"Monster with id {id} not found")
    return monster


def _get_user_by_id(id: int, db: Session) -> User:
    user = db.query(User).filter(User.discord_id == id).first()
    if user is None:
        raise UserNotFoundError(f"User with id {id} not found")
    return user


def _get_monster_by_name(name: str, db: Session) -> Monster:
    monster = db.query(Monster).filter(Monster.monster_name == name).first()
    if monster is None:
        raise UserNotFoundError(f"Monster with name {name} not found")
    return monster


def _update_dict_field(monster_field: dict, update_field: dict):
    if monster_field is not None and update_field is not None:
        monster_field.update(update_field)


def create_new_monster(monster: MonsterCreate, db: Session) -> Monster:
    monster_orm = Monster(
        monster_name=monster.monster_name,
        race=monster.race,
        gender=monster.gender,
        pace=monster.pace,
        charisma=monster.charisma,
        parry=monster.parry,
        toughness=monster.toughness,
        attributes=monster.attributes,
        skills=monster.skills,
        gear=monster.gear,
        hindrances=monster.hindrances,
        edges=monster.edges,
        powers=monster.powers,
        weapons=monster.weapons,
        damage=monster.damage,
        ammo=monster.ammo,
        money=monster.money,
    )
    db.add(monster_orm)
    db.commit()
    db.refresh(monster_orm)
    db.commit()

    return monster_orm


def retrieve_monster(id: int, db: Session) -> Optional[Monster]:
    try:
        return _get_monster_by_id(id, db)
    except MonsterNotFoundError:
        return None


def retrieve_user_monster(id: int, name: str, db: Session) -> Optional[Monster]:
    user = _get_user_by_id(id, db)
    monster = _get_monster_by_name(name, db)

    if monster.user_id != user.discord_id:
        raise MonsterNotFoundError(
            f"Monster with name {name} does not belong to user with id {id}"
        )

    return monster


def list_monsters(db: Session) -> List[Monster]:
    rows = db.query(Monster).all()
    return rows if rows else []


def list_user_monsters(id: int, db: Session) -> List[Monster]:
    user = _get_user_by_id(id, db)
    rows = db.query(Monster).filter(Monster.user_id == user.discord_id).all()
    return rows if rows else []


def update_monster(monster_id: int, monster: UpdateMonster, db: Session) -> Monster:
    row = _get_monster_by_id(monster_id, db)

    _update_dict_field(row.attributes, monster.attributes)
    _update_dict_field(row.skills, monster.skills)
    _update_dict_field(row.gear, monster.gear)
    _update_dict_field(row.damage, monster.damage)

    for var, value in monster.dict(
        exclude={"attributes", "skills", "gear", "damage"}, exclude_unset=True
    ).items():
        setattr(row, var, value)

    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def delete_monster(id: int, db: Session) -> Monster:
    monster = _get_monster_by_id(id, db)
    db.delete(monster)
    db.commit()
    return monster


def add_gear_to_monster(
    monster_name: str, gear_name: str, amount: int, db: Session
) -> Monster:
    monster = _get_monster_by_name(monster_name, db)
    gear = retrieve_gear(gear_name, db)

    stmt = gear_monster.insert().values(
        monster_id=monster.id, gear_id=gear.id, quantity=amount
    )
    db.execute(stmt)
    db.commit()
    db.commit()

    return monster


def add_power_to_monster(monster_id: int, power_id: int, db: Session) -> Monster:
    monster = _get_monster_by_id(monster_id, db)
    power = retrieve_power(power_id, db)

    monster.powers.append(power)
    db.commit()

    return monster


def add_weapon_to_monster(
    monster_name: str, weapon_name: str, amount: int, db: Session
) -> Monster:
    monster = _get_monster_by_name(monster_name, db)
    weapon = retrieve_weapon(weapon_name, db)

    stmt = weapon_monster.insert().values(
        monster_id=monster.id, weapon_id=weapon.id, quantity=amount
    )
    db.execute(stmt)
    db.commit()

    return monster


def add_monster_to_encounter(
    monster_id: int, encounter_id: int, db: Session
) -> Monster:
    monster = _get_monster_by_id(monster_id, db)
    encounter = retrieve_encounter(encounter_id, db)

    monster.encounters.append(encounter)
    db.commit()

    return monster


def has_enough_money(user_id: int, monster_name: str, amount: int, db: Session) -> bool:
    monster = retrieve_user_monster(user_id, monster_name, db)
    return monster.money >= amount


def add_money_to_monster(
    user_id: int, monster_name: str, amount: int, db: Session
) -> Monster:
    monster = retrieve_user_monster(user_id, monster_name, db)

    monster.money += amount
    db.commit()

    return monster


def subtract_money_to_monster(
    user_id: int, monster_name: str, amount: int, db: Session
) -> Monster:
    if not has_enough_money(user_id, monster_name, amount, db):
        raise ValueError(f"Monster {monster_name} does not have enough money")

    monster = retrieve_user_monster(user_id, monster_name, db)
    monster.money -= amount
    db.commit()

    return monster


def check_money_for_monster(user_id: int, monster_name: str, db: Session) -> int:
    monster = retrieve_user_monster(user_id, monster_name, db)
    db.commit()

    return monster.money
