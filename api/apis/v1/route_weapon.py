from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas.weapon import WeaponCreate, ShowWeapon, UpdateWeapon
from db.session import get_db
from db.repository.character import retrieve_character
from db.repository.monster import retrieve_monster
from db.repository.weapon import (
    create_new_weapon,
    retrieve_weapon,
    list_weapons,
    update_weapon,
    delete_weapon,
)

router = APIRouter()


@router.post("/weapons", response_model=ShowWeapon, status_code=status.HTTP_201_CREATED)
def create_a_weapon(weapon: WeaponCreate, db: Session = Depends(get_db)):
    weapon = create_new_weapon(weapon=weapon, db=db)
    return weapon


@router.get("/weapons", response_model=List[ShowWeapon], status_code=status.HTTP_200_OK)
def get_all_weapons(db: Session = Depends(get_db)):
    weapons = list_weapons(db=db)
    return weapons


@router.get("/weapons/{id}", response_model=ShowWeapon, status_code=status.HTTP_200_OK)
def get_a_weapon(id: int, db: Session = Depends(get_db)):
    weapon = retrieve_weapon(weapon_id=id, db=db)
    if not weapon:
        raise HTTPException(
            detail=f"Weapon with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return weapon


@router.put("/weapons/{id}", response_model=ShowWeapon, status_code=status.HTTP_200_OK)
def update_a_weapon(id: int, weapon: UpdateWeapon, db: Session = Depends(get_db)):
    weapon = update_weapon(weapon_id=id, weapon=weapon, db=db)
    if not weapon:
        raise HTTPException(
            detail=f"Weapon with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return weapon


@router.delete(
    "/weapons/{id}", response_model=ShowWeapon, status_code=status.HTTP_200_OK
)
def delete_a_weapon(id: int, db: Session = Depends(get_db)):
    weapon = delete_weapon(weapon_id=id, db=db)
    if not weapon:
        raise HTTPException(
            detail=f"Weapon with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return weapon


@router.post("/weapons/characters/{id}", status_code=status.HTTP_201_CREATED)
def add_weapon_to_character(
    id: int, weapon_ids: List[int], db: Session = Depends(get_db)
):
    character = retrieve_character(id=id, db=db)
    if not character:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for weapon_id in weapon_ids:
        weapon = retrieve_weapon(weapon_id, db=db)
        if not weapon:
            raise HTTPException(
                detail=f"Weapon with id {weapon_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        character.weapons.append(weapon)

    db.commit()

    return character


@router.delete("/weapons/characters/{id}", status_code=status.HTTP_200_OK)
def remove_weapon_from_character(
    id: int, weapon_ids: List[int], db: Session = Depends(get_db)
):
    character = retrieve_character(id=id, db=db)
    if not character:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for weapon_id in weapon_ids:
        weapon = retrieve_weapon(weapon_id, db=db)
        if not weapon:
            raise HTTPException(
                detail=f"Weapon with id {weapon_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if weapon in character.weapons:
            character.weapons.remove(weapon)

    db.commit()

    return character


@router.post("/weapons/monsters/{id}", status_code=status.HTTP_201_CREATED)
def add_weapon_to_monster(
    id: int, weapon_ids: List[int], db: Session = Depends(get_db)
):
    monster = retrieve_monster(id=id, db=db)
    if not monster:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for weapon_id in weapon_ids:
        weapon = retrieve_weapon(weapon_id, db=db)
        if not weapon:
            raise HTTPException(
                detail=f"Weapon with id {weapon_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        monster.weapons.append(weapon)

    db.commit()

    return monster


@router.delete("/weapons/monsters/{id}", status_code=status.HTTP_200_OK)
def remove_weapon_from_monster(
    id: int, weapon_ids: List[int], db: Session = Depends(get_db)
):
    monster = retrieve_monster(id=id, db=db)
    if not monster:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for weapon_id in weapon_ids:
        weapon = retrieve_weapon(weapon_id, db=db)
        if not weapon:
            raise HTTPException(
                detail=f"Weapon with id {weapon_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if weapon in monster.weapons:
            monster.weapons.remove(weapon)

    db.commit()

    return monster
