from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

# from schemas.character import ShowCharacter
from schemas.encounter import (
    EncounterCreate,
    ShowEncounter,
    UpdateEncounter,
    ShowEncounterCharacter,
    ShowEncounterMonster,
)
from db.session import get_db
from db.repository.character import retrieve_character
from db.repository.monster import retrieve_monster
from db.repository.encounter import (
    create_new_encounter,
    retrieve_encounter,
    list_characters,
    list_encounters,
    list_monsters,
    update_encounter,
    delete_encounter,
)

router = APIRouter()


@router.post(
    "/encounters", response_model=ShowEncounter, status_code=status.HTTP_201_CREATED
)
def create_an_encounter(encounter: EncounterCreate, db: Session = Depends(get_db)):
    encounter = create_new_encounter(encounter=encounter, db=db)
    return encounter


@router.get(
    "/encounters", response_model=List[ShowEncounter], status_code=status.HTTP_200_OK
)
def get_all_encounters(db: Session = Depends(get_db)):
    encounters = list_encounters(db=db)
    return encounters


@router.get(
    "/encounters/{id}", response_model=ShowEncounter, status_code=status.HTTP_200_OK
)
def get_an_encounter(id: int, db: Session = Depends(get_db)):
    encounter = retrieve_encounter(encounter_id=id, db=db)
    if not encounter:
        raise HTTPException(
            detail=f"Encounter with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return encounter


@router.put(
    "/encounters/{id}", response_model=ShowEncounter, status_code=status.HTTP_200_OK
)
def update_an_encounter(
    id: int, encounter: UpdateEncounter, db: Session = Depends(get_db)
):
    encounter = update_encounter(encounter_id=id, encounter=encounter, db=db)
    if not encounter:
        raise HTTPException(
            detail=f"Encounter with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return encounter


@router.delete(
    "/encounters/{id}", response_model=ShowEncounter, status_code=status.HTTP_200_OK
)
def delete_an_encounter(id: int, db: Session = Depends(get_db)):
    encounter = delete_encounter(encounter_id=id, db=db)
    if not encounter:
        raise HTTPException(
            detail=f"Encounter with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return encounter


@router.get(
    "/encounters/{id}/characters",
    response_model=List[ShowEncounterCharacter],
    status_code=status.HTTP_200_OK,
)
def get_characters_in_encounter(id: int, db: Session = Depends(get_db)):
    characters = list_characters(id, db)
    if not characters:
        raise HTTPException(
            detail=f"No characters added to encounter id {id} yet",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return characters


@router.get(
    "/encounters/{id}/monsters",
    response_model=List[ShowEncounterMonster],
    status_code=status.HTTP_200_OK,
)
def get_monsters_in_encounter(id: int, db: Session = Depends(get_db)):
    monsters = list_monsters(id, db)
    if not monsters:
        raise HTTPException(
            detail=f"No monsters added to encounter id {id} yet",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return monsters


@router.post("/encounters/characters/{id}", status_code=status.HTTP_201_CREATED)
def add_character_to_encounter(
    id: int, encounter_ids: List[int], db: Session = Depends(get_db)
):
    character = retrieve_character(id=id, db=db)
    if not character:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for encounter_id in encounter_ids:
        encounter = retrieve_encounter(encounter_id, db=db)
        if not encounter:
            raise HTTPException(
                detail=f"Power with id {encounter_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        character.encounters.append(encounter)

    db.commit()

    return character


@router.delete("/encounters/characters/{id}", status_code=status.HTTP_200_OK)
def remove_character_from_encounter(
    id: int, encounter_ids: List[int], db: Session = Depends(get_db)
):
    character = retrieve_character(id=id, db=db)
    if not character:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for encounter_id in encounter_ids:
        encounter = retrieve_encounter(encounter_id, db=db)
        if not encounter:
            raise HTTPException(
                detail=f"Weapon with id {encounter_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if encounter in character.encounters:
            character.encounters.remove(encounter)

    db.commit()

    return character


@router.post("/encounters/monsters/{id}", status_code=status.HTTP_201_CREATED)
def add_monster_to_encounter(
    id: int, encounter_ids: List[int], db: Session = Depends(get_db)
):
    monster = retrieve_monster(id=id, db=db)
    if not monster:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for encounter_id in encounter_ids:
        encounter = retrieve_encounter(encounter_id, db=db)
        if not encounter:
            raise HTTPException(
                detail=f"Power with id {encounter_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        monster.encounters.append(encounter)

    db.commit()

    return monster


@router.delete("/encounters/monsters/{id}", status_code=status.HTTP_200_OK)
def remove_monster_from_encounter(
    id: int, encounter_ids: List[int], db: Session = Depends(get_db)
):
    monster = retrieve_monster(id=id, db=db)
    if not monster:
        raise HTTPException(
            detail=f"Character with id {id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    for encounter_id in encounter_ids:
        encounter = retrieve_encounter(encounter_id, db=db)
        if not encounter:
            raise HTTPException(
                detail=f"Weapon with id {encounter_id} not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if encounter in monster.encounters:
            monster.encounters.remove(encounter)

    db.commit()

    return monster
