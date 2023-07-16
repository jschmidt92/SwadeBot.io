from sqlalchemy.orm import Session
from typing import Union, List, Optional

from db.models.power import Power
from db.repository.utilities import _get_power_by_id
from schemas.power import PowerCreate, UpdatePower


def create_new_power(power: PowerCreate, db: Session) -> Power:
    power_orm = Power(
        name=power.name,
        pp=power.pp,
        range=power.range,
        duration=power.duration,
        effect=power.effect,
        notes=power.notes,
    )
    db.add(power_orm)
    db.commit()
    db.refresh(power_orm)
    return power_orm


def retrieve_power(power_identifier: Union[int, str], db: Session) -> Optional[Power]:
    if isinstance(power_identifier, int):
        row = _get_power_by_id(power_identifier, db)
    elif isinstance(power_identifier, str):
        row = db.query(Power).filter(Power.name == power_identifier).first()
    else:
        return None

    if row is None:
        return None
    return row


def list_powers(db: Session) -> List[Power]:
    rows = db.query(Power).all()
    return rows if rows else []


def update_power(power_id: int, power: UpdatePower, db: Session) -> Power:
    power_data = _get_power_by_id(power_id, db)
    for var, value in power.dict(exclude_unset=True).items():
        setattr(power_data, var, value)
    db.commit()
    db.refresh(power_data)
    return power_data


def delete_power(power_id: int, db: Session) -> Power:
    power = _get_power_by_id(power_id, db)
    db.delete(power)
    db.commit()
    return power
