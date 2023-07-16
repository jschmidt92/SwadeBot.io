from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas.character import ShowCharacter
from schemas.user import UserCreate, ShowUser, UpdateUser
from db.session import get_db
from db.repository.character import list_user_characters, retrieve_user_character
from db.repository.user import (
    create_new_user,
    retrieve_user,
    list_users,
    update_user,
    delete_user,
)

router = APIRouter()


@router.post("/users", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_a_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user


@router.get("/users", response_model=List[ShowUser], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    users = list_users(db=db)
    return users


@router.get("/users/{id}", response_model=ShowUser, status_code=status.HTTP_200_OK)
def get_a_user(id: int, db: Session = Depends(get_db)):
    user = retrieve_user(discord_id=id, db=db)
    if not user:
        raise HTTPException(
            detail=f"User with id {id} not found", status_code=status.HTTP_404_NOT_FOUND
        )
    return user


@router.put("/users/{id}", response_model=ShowUser, status_code=status.HTTP_200_OK)
def update_a_user(id: int, user: UpdateUser, db: Session = Depends(get_db)):
    user = update_user(user_id=id, user=user, db=db)
    if not user:
        raise HTTPException(
            detail=f"User with id {id} not found", status_code=status.HTTP_404_NOT_FOUND
        )
    return user


@router.delete("/users/{id}", response_model=ShowUser, status_code=status.HTTP_200_OK)
def delete_a_user(id: int, db: Session = Depends(get_db)):
    user = delete_user(user_id=id, db=db)
    if not user:
        raise HTTPException(
            detail=f"User with id {id} not found", status_code=status.HTTP_404_NOT_FOUND
        )
    return user


@router.get(
    "/users/{id}/characters",
    response_model=List[ShowCharacter],
    status_code=status.HTTP_200_OK,
)
def get_all_characters_for_user(id: int, db: Session = Depends(get_db)):
    characters = list_user_characters(id=id, db=db)
    return characters


@router.get(
    "/users/{id}/characters/{name}",
    response_model=ShowCharacter,
    status_code=status.HTTP_200_OK,
)
def get_a_character_for_user(id: int, name: str, db: Session = Depends(get_db)):
    character = retrieve_user_character(id=id, name=name, db=db)
    if not character or character.user_id != id:
        raise HTTPException(
            detail=f"Character with id {name} not found for user {id}",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return character
