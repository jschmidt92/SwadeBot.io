from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from schemas.character import CharacterCreate, ShowCharacter, UpdateCharacter
from schemas.money import MoneyCheck, MoneyInput
from db.models.character import Race, Gender
from db.repository.character import (
    add_money_to_character,
    subtract_money_to_character,
    check_money_for_character,
    create_new_character,
    retrieve_character,
    list_characters,
    update_character,
    delete_character,
)
from db.session import get_db


router = APIRouter()


@router.post(
    "/characters", response_model=ShowCharacter, status_code=status.HTTP_200_OK
)
def create_a_character(character: CharacterCreate, db: Session = Depends(get_db)):
    character = create_new_character(character=character, db=db)
    return character


@router.get(
    "/characters", response_model=List[ShowCharacter], status_code=status.HTTP_200_OK
)
def get_all_characters(db: Session = Depends(get_db)):
    characters = list_characters(db=db)
    return characters


@router.get(
    "/characters/{id}", response_model=ShowCharacter, status_code=status.HTTP_200_OK
)
def get_a_character(id: int, db: Session = Depends(get_db)):
    character = retrieve_character(id=id, db=db)
    if not character:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return character


@router.post(
    "/characters/add_money",
    response_model=ShowCharacter,
    status_code=status.HTTP_200_OK,
)
def add_money(data: MoneyInput, db: Session = Depends(get_db)):
    character = add_money_to_character(
        user_id=data.user_id,
        character_name=data.character_name,
        amount=data.amount,
        db=db,
    )
    if not character or character.user_id != data.user_id:
        raise HTTPException(
            detail=f"Character with name {data.character_name} not found for user {data.user_id}",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return character


@router.post(
    "/characters/subtract_money",
    response_model=ShowCharacter,
    status_code=status.HTTP_200_OK,
)
def subtract_money(data: MoneyInput, db: Session = Depends(get_db)):
    character = subtract_money_to_character(
        user_id=data.user_id,
        character_name=data.character_name,
        amount=data.amount,
        db=db,
    )
    if not character or character.user_id != data.user_id:
        raise HTTPException(
            detail=f"Character with name {data.character_name} not found for user {data.user_id}",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return character


@router.put(
    "/characters/check_money",
    response_model=int,
    status_code=status.HTTP_200_OK,
)
def check_money(data: MoneyCheck, db: Session = Depends(get_db)):
    money = check_money_for_character(
        user_id=data.user_id, character_name=data.character_name, db=db
    )
    if money is None:
        raise HTTPException(
            detail=f"Character with name {data.character_name} not found for user {data.user_id}",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return money


@router.put(
    "/characters/{id}", response_model=ShowCharacter, status_code=status.HTTP_200_OK
)
def update_a_character(
    id: int, character: UpdateCharacter, db: Session = Depends(get_db)
):
    character = update_character(id=id, character=character, db=db)
    if not character:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return character


@router.delete(
    "/characters/{id}", response_model=ShowCharacter, status_code=status.HTTP_200_OK
)
def delete_a_character(id: int, db: Session = Depends(get_db)):
    character = delete_character(id=id, db=db)
    if not character:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return character
