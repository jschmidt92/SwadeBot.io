from sqlalchemy.orm import Session
from typing import Union, List, Optional

from db.models.weapon import Weapon
from schemas.weapon import WeaponCreate, UpdateWeapon


class WeaponNotFoundError(Exception):
    pass


def _get_weapon_by_id(weapon_id: int, db: Session) -> Weapon:
    weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
    if weapon is None:
        raise WeaponNotFoundError(f"Weapon with id {weapon_id} not found")
    return weapon


def create_new_weapon(weapon: WeaponCreate, db: Session) -> Weapon:
    weapon_orm = Weapon(
        name=weapon.name,
        range=weapon.range,
        damage=weapon.damage,
        rof=weapon.rof,
        shots=weapon.shots,
        min_str=weapon.min_str,
        wt=weapon.wt,
        cost=weapon.cost,
        notes=weapon.notes,
    )
    db.add(weapon_orm)
    db.commit()
    db.refresh(weapon_orm)
    return weapon_orm


def retrieve_weapon(
    weapon_identifier: Union[int, str], db: Session
) -> Optional[Weapon]:
    if isinstance(weapon_identifier, int):
        row = _get_weapon_by_id(weapon_identifier, db)
    elif isinstance(weapon_identifier, str):
        row = db.query(Weapon).filter(Weapon.name == weapon_identifier).first()
    else:
        return None

    if row is None:
        return None
    return row


def list_weapons(db: Session) -> List[Weapon]:
    rows = db.query(Weapon).all()
    return rows if rows else []


def update_weapon(weapon_id: int, weapon: UpdateWeapon, db: Session) -> Weapon:
    weapon_data = _get_weapon_by_id(weapon_id, db)
    for var, value in weapon.dict(exclude_unset=True).items():
        setattr(weapon_data, var, value)
    db.commit()
    db.refresh(weapon_data)
    return weapon_data


def update_weapon(weapon_id: int, weapon: UpdateWeapon, db: Session):
    weapon_data = db.query(Weapon).filter(Weapon.id == weapon_id).first()
    if weapon_data is None:
        return None
    for var, value in weapon.dict(exclude_unset=True).items():
        setattr(weapon_data, var, value)
    db.commit()
    db.refresh(weapon_data)
    return weapon_data


def delete_weapon(weapon_id: int, db: Session) -> Weapon:
    weapon = _get_weapon_by_id(weapon_id, db)
    db.delete(weapon)
    db.commit()
    return weapon
