from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas.gear import GearCreate, ShowGear, UpdateGear
from db.session import get_db
from db.repository.character import retrieve_character
from db.repository.monster import retrieve_monster
from db.repository.gear import (
    create_new_gear,
    retrieve_gear,
    list_gear,
    update_gear,
    delete_gear,
)

router = APIRouter()


@router.post("/gear", response_model=ShowGear, status_code=status.HTTP_201_CREATED)
def create_a_gear(gear: GearCreate, db: Session = Depends(get_db)):
    gear = create_new_gear(gear=gear, db=db)
    return gear


@router.get("/gear", response_model=List[ShowGear], status_code=status.HTTP_200_OK)
def get_all_gear(db: Session = Depends(get_db)):
    gear = list_gear(db=db)
    return gear


@router.get("/gear/{id}", response_model=ShowGear, status_code=status.HTTP_200_OK)
def get_a_gear(id: int, db: Session = Depends(get_db)):
    gear = retrieve_gear(gear_id=id, db=db)
    if not gear:
        raise HTTPException(
            detail=f"Gear with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return gear


@router.put("/gear/{id}", response_model=ShowGear, status_code=status.HTTP_200_OK)
def update_a_gear(id: int, gear: UpdateGear, db: Session = Depends(get_db)):
    gear = update_gear(gear_id=id, gear=gear, db=db)
    if not gear:
        raise HTTPException(
            detail=f"Gear with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return gear


@router.delete("/gear/{id}", response_model=ShowGear, status_code=status.HTTP_200_OK)
def delete_a_gear(id: int, db: Session = Depends(get_db)):
    gear = delete_gear(gear_id=id, db=db)
    if not gear:
        raise HTTPException(
            detail=f"Gear with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return gear


@router.post("/gear/characters/{id}", status_code=status.HTTP_201_CREATED)
def add_gear_to_character(id: int, gear_ids: List[int], db: Session = Depends(get_db)):
    character = retrieve_character(id=id, db=db)
    if not character:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for gear_id in gear_ids:
        gear = retrieve_gear(gear_id, db=db)
        if not gear:
            raise HTTPException(
                detail=f"Power with id {gear_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        character.gear.append(gear)

    db.commit()

    return character


@router.delete("/gear/characters/{id}", status_code=status.HTTP_200_OK)
def remove_gear_from_character(
    id: int, gear_ids: List[int], db: Session = Depends(get_db)
):
    character = retrieve_character(id=id, db=db)
    if not character:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for gear_id in gear_ids:
        gear = retrieve_gear(gear_id, db=db)
        if not gear:
            raise HTTPException(
                detail=f"Weapon with id {gear_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if gear in character.gear:
            character.gear.remove(gear)

    db.commit()

    return character


@router.post("/gear/monsters/{id}", status_code=status.HTTP_201_CREATED)
def add_gear_to_monster(id: int, gear_ids: List[int], db: Session = Depends(get_db)):
    monster = retrieve_monster(id=id, db=db)
    if not monster:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for gear_id in gear_ids:
        gear = retrieve_gear(gear_id, db=db)
        if not gear:
            raise HTTPException(
                detail=f"Power with id {gear_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        monster.gear.append(gear)

    db.commit()

    return monster


@router.delete("/gear/monsters/{id}", status_code=status.HTTP_200_OK)
def remove_gear_from_monster(
    id: int, gear_ids: List[int], db: Session = Depends(get_db)
):
    monster = retrieve_monster(id=id, db=db)
    if not monster:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for gear_id in gear_ids:
        gear = retrieve_gear(gear_id, db=db)
        if not gear:
            raise HTTPException(
                detail=f"Weapon with id {gear_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if gear in monster.weapons:
            monster.weapons.remove(gear)

    db.commit()

    return monster
