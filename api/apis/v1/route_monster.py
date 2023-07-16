from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from schemas.monster import MonsterCreate, ShowMonster, UpdateMonster
from schemas.money import MoneyCheck, MoneyInput
from db.models.monster import Race, Gender
from db.repository.monster import (
    add_money_to_monster,
    subtract_money_to_monster,
    check_money_for_monster,
    create_new_monster,
    retrieve_monster,
    list_monsters,
    update_monster,
    delete_monster,
)
from db.session import get_db


router = APIRouter()


@router.post("/monsters", response_model=ShowMonster, status_code=status.HTTP_200_OK)
def create_a_monster(monster: MonsterCreate, db: Session = Depends(get_db)):
    monster = create_new_monster(monster=monster, db=db)
    return monster


@router.get(
    "/monsters", response_model=List[ShowMonster], status_code=status.HTTP_200_OK
)
def get_all_monsters(db: Session = Depends(get_db)):
    monsters = list_monsters(db=db)
    return monsters


@router.get(
    "/monsters/{id}", response_model=ShowMonster, status_code=status.HTTP_200_OK
)
def get_a_monster(id: int, db: Session = Depends(get_db)):
    monster = retrieve_monster(id=id, db=db)
    if not monster:
        raise HTTPException(
            detail=f"Monster with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return monster


@router.put(
    "/monsters/{id}", response_model=ShowMonster, status_code=status.HTTP_200_OK
)
def update_a_monster(id: int, monster: UpdateMonster, db: Session = Depends(get_db)):
    monster = update_monster(id=id, monster=monster, db=db)
    if not monster:
        raise HTTPException(
            detail=f"Monster with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return monster


@router.delete(
    "/monsters/{id}", response_model=ShowMonster, status_code=status.HTTP_200_OK
)
def delete_a_monster(id: int, db: Session = Depends(get_db)):
    monster = delete_monster(id=id, db=db)
    if not monster:
        raise HTTPException(
            detail=f"Monster with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return monster
