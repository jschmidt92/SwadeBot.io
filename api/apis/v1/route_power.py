from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas.power import PowerCreate, ShowPower, UpdatePower
from db.session import get_db
from db.repository.character import retrieve_character
from db.repository.monster import retrieve_monster
from db.repository.power import (
    create_new_power,
    retrieve_power,
    list_powers,
    update_power,
    delete_power,
)

router = APIRouter()


@router.post("/powers", response_model=ShowPower, status_code=status.HTTP_201_CREATED)
def create_a_power(power: PowerCreate, db: Session = Depends(get_db)):
    power = create_new_power(power=power, db=db)
    return power


@router.get("/powers", response_model=List[ShowPower], status_code=status.HTTP_200_OK)
def get_all_powers(db: Session = Depends(get_db)):
    powers = list_powers(db=db)
    return powers


@router.put("/powers/{id}", response_model=ShowPower, status_code=status.HTTP_200_OK)
def update_a_power(id: int, power: UpdatePower, db: Session = Depends(get_db)):
    power = update_power(power_id=id, power=power, db=db)
    if not power:
        raise HTTPException(
            detail=f"Power with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return power


@router.get("/powers/{id}", response_model=ShowPower, status_code=status.HTTP_200_OK)
def get_a_power(id: int, db: Session = Depends(get_db)):
    power = retrieve_power(power_id=id, db=db)
    if not power:
        raise HTTPException(
            detail=f"Power with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return power


@router.delete("/powers/{id}", response_model=ShowPower, status_code=status.HTTP_200_OK)
def delete_a_power(id: int, db: Session = Depends(get_db)):
    power = delete_power(power_id=id, db=db)
    if not power:
        raise HTTPException(
            detail=f"Power with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return power


@router.post("/powers/characters/{id}", status_code=status.HTTP_201_CREATED)
def add_power_to_character(
    id: int, power_ids: List[int], db: Session = Depends(get_db)
):
    character = retrieve_character(id=id, db=db)
    if not character:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for power_id in power_ids:
        power = retrieve_power(power_id, db=db)
        if not power:
            raise HTTPException(
                detail=f"Power with id {power_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        character.powers.append(power)

    db.commit()

    return character


@router.delete("/powers/characters/{id}", status_code=status.HTTP_200_OK)
def remove_power_from_character(
    id: int, power_ids: List[int], db: Session = Depends(get_db)
):
    character = retrieve_character(id=id, db=db)
    if not character:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for power_id in power_ids:
        power = retrieve_power(power_id, db=db)
        if not power:
            raise HTTPException(
                detail=f"Weapon with id {power_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if power in character.weapons:
            character.weapons.remove(power)

    db.commit()

    return character


@router.post("/powers/monsters/{id}", status_code=status.HTTP_201_CREATED)
def add_power_to_monster(id: int, power_ids: List[int], db: Session = Depends(get_db)):
    monster = retrieve_monster(id=id, db=db)
    if not monster:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for power_id in power_ids:
        power = retrieve_power(power_id, db=db)
        if not power:
            raise HTTPException(
                detail=f"Power with id {power_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        monster.powers.append(power)

    db.commit()

    return monster


@router.delete("/powers/monsters/{id}", status_code=status.HTTP_200_OK)
def remove_power_from_monster(
    id: int, power_ids: List[int], db: Session = Depends(get_db)
):
    monster = retrieve_monster(id=id, db=db)
    if not monster:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for power_id in power_ids:
        power = retrieve_power(power_id, db=db)
        if not power:
            raise HTTPException(
                detail=f"Weapon with id {power_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if power in monster.weapons:
            monster.weapons.remove(power)

    db.commit()

    return monster
