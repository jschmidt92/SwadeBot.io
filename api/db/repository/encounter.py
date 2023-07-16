from sqlalchemy.orm import Session
from sqlalchemy import join, select
from typing import List, Optional

from db.models.association import encounter_character, encounter_monster
from db.models.character import Character
from db.models.encounter import Encounter
from db.models.monster import Monster
from schemas.encounter import EncounterCreate, UpdateEncounter


class EncounterNotFoundError(Exception):
    pass


def _get_encounter_by_id(encounter_id: int, db: Session) -> Encounter:
    encounter = db.query(Encounter).filter(Encounter.id == encounter_id).first()
    if encounter is None:
        raise EncounterNotFoundError(f"Encounter with id {encounter_id} not found")
    return encounter


def create_new_encounter(encounter: EncounterCreate, db: Session) -> Encounter:
    encounter_orm = Encounter(
        name=encounter.name,
        notes=encounter.notes,
    )
    db.add(encounter_orm)
    db.commit()
    db.refresh(encounter_orm)
    return encounter_orm


def retrieve_encounter(encounter_id: int, db: Session) -> Optional[Encounter]:
    if isinstance(encounter_id, int):
        row = _get_encounter_by_id(encounter_id, db)
    else:
        return None

    if row is None:
        return None
    return row


def list_encounters(db: Session) -> List[Encounter]:
    rows = db.query(Encounter).all()
    return rows if rows else []


def update_encounter(
    encounter_id: int, encounter: UpdateEncounter, db: Session
) -> Encounter:
    encounter_data = _get_encounter_by_id(encounter_id, db)
    for var, value in encounter.dict(exclude_unset=True).items():
        setattr(encounter_data, var, value)
    db.commit()
    db.refresh(encounter_data)
    return encounter_data


def update_encounter(encounter_id: int, encounter: UpdateEncounter, db: Session):
    encounter_data = db.query(Encounter).filter(Encounter.id == encounter_id).first()
    if encounter_data is None:
        return None
    for var, value in encounter.dict(exclude_unset=True).items():
        setattr(encounter_data, var, value)
    db.commit()
    db.refresh(encounter_data)
    return encounter_data


def delete_encounter(encounter_id: int, db: Session) -> Encounter:
    encounter = _get_encounter_by_id(encounter_id, db)
    db.delete(encounter)
    db.commit()
    return encounter


def list_characters(encounter_id: int, db: Session) -> List[Character]:
    encounter = _get_encounter_by_id(encounter_id, db)
    stmt = (
        select(Character)
        .select_from(
            join(
                Character,
                encounter_character,
                Character.id == encounter_character.c.character_id,
            )
        )
        .where(encounter_character.c.encounter_id == encounter.id)
    )

    result = db.execute(stmt).scalars().all()
    return result


def list_monsters(encounter_id: int, db: Session) -> List[Monster]:
    encounter = _get_encounter_by_id(encounter_id, db)
    stmt = (
        select(Monster)
        .select_from(
            join(
                Monster,
                encounter_monster,
                Monster.id == encounter_monster.c.monster_id,
            )
        )
        .where(encounter_monster.c.encounter_id == encounter.id)
    )

    result = db.execute(stmt).scalars().all()
    return result
