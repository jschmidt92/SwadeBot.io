from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.repository.character import add_gear_to_character
from db.repository.store import (
    buy_gear,
    buy_weapon,
    list_gear,
    list_weapons,
    sell_gear,
    sell_weapon,
)
from db.session import get_db

from schemas.character import ShowCharacter
from schemas.gear import ShowGear
from schemas.store import GearInput, WeaponInput
from schemas.weapon import ShowWeapon

router = APIRouter()


@router.get(
    "/store/gear", response_model=List[ShowGear], status_code=status.HTTP_200_OK
)
def get_all_gear(db: Session = Depends(get_db)):
    rows = list_gear(db=db)
    return rows


@router.get(
    "/store/weapons", response_model=List[ShowWeapon], status_code=status.HTTP_200_OK
)
def get_all_weapons(db: Session = Depends(get_db)):
    rows = list_weapons(db=db)
    return rows


@router.put(
    "/store/character/buy_gear",
    status_code=status.HTTP_200_OK,
)
def buy_gear_for_character(data: GearInput, db: Session = Depends(get_db)):
    character = buy_gear(
        user_id=data.user_id,
        character_name=data.character_name,
        gear_name=data.gear_name,
        amount=data.amount,
        db=db,
    )
    if not character or character.user_id != data.user_id:
        raise HTTPException(
            detail=f"Character with name {data.character_name} not found for {data.user_id}",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return character


@router.put("/store/character/sell_gear", status_code=status.HTTP_200_OK)
def sell_gear_for_character(
    character_id: int, gear_id: int, db: Session = Depends(get_db)
):
    try:
        character = sell_gear(character_id=character_id, gear_id=gear_id, db=db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return character


@router.put("/store/character/buy_weapon", status_code=status.HTTP_200_OK)
def buy_weapon_for_character(data: WeaponInput, db: Session = Depends(get_db)):
    character = buy_weapon(
        user_id=data.user_id,
        character_name=data.character_name,
        weapon_name=data.weapon_name,
        amount=data.amount,
        db=db,
    )
    if not character or character.user_id != data.user_id:
        raise HTTPException(
            detail=f"Character with name {data.character_name} not found for {data.user_id}",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return character


@router.put("/store/character/sell_weapon", status_code=status.HTTP_200_OK)
def sell_weapon_for_character(
    character_id: int, weapon_id: int, db: Session = Depends(get_db)
):
    try:
        character = sell_weapon(character_id=character_id, weapon_id=weapon_id, db=db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return character
