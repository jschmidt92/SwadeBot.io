from sqlalchemy.orm import Session
from typing import Union, List, Optional

from db.models.gear import Gear
from db.repository.utilities import _get_gear_by_id
from schemas.gear import GearCreate, UpdateGear


def create_new_gear(gear: GearCreate, db: Session) -> Gear:
    gear_orm = Gear(
        name=gear.name,
        min_str=gear.min_str,
        wt=gear.wt,
        cost=gear.cost,
        notes=gear.notes,
    )
    db.add(gear_orm)
    db.commit()
    db.refresh(gear_orm)
    return gear_orm


def retrieve_gear(gear_identifier: Union[int, str], db: Session) -> Optional[Gear]:
    if isinstance(gear_identifier, int):
        row = _get_gear_by_id(gear_identifier, db)
    elif isinstance(gear_identifier, str):
        row = db.query(Gear).filter(Gear.name == gear_identifier).first()
    else:
        return None

    if row is None:
        return None
    return row


def list_gear(db: Session) -> List[Gear]:
    rows = db.query(Gear).all()
    return rows if rows else []


def update_gear(gear_id: int, gear: UpdateGear, db: Session) -> Gear:
    gear_data = _get_gear_by_id(gear_id, db)
    for var, value in gear.dict(exclude_unset=True).items():
        setattr(gear_data, var, value)
    db.commit()
    db.refresh(gear_data)
    return gear_data


def delete_gear(gear_id: int, db: Session) -> Gear:
    gear = _get_gear_by_id(gear_id, db)
    db.delete(gear)
    db.commit()
    return gear
