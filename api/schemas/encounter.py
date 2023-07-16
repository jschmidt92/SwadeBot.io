from pydantic import BaseModel, Field
from typing import List, Optional, Any


class EncounterCreate(BaseModel):
    name: Optional[str] = Field(...)
    notes: Optional[str] = Field(...)


class UpdateEncounter(BaseModel):
    name: Optional[str]
    notes: Optional[str]


class ShowEncounter(BaseModel):
    id: Optional[int]
    name: Optional[str]
    notes: Optional[str]
    characters: Optional[list]
    monsters: Optional[list]

    class Config:
        orm_mode = True


class ShowEncounterCharacter(BaseModel):
    id: Optional[int]
    character_name: Optional[str]
    charisma: Optional[int]
    pace: Optional[int]
    parry: Optional[int]
    toughness: Optional[int]
    attributes: Optional[dict]
    skills: Optional[dict]
    gear: Optional[list]
    hindrances: Optional[str]
    edges: Optional[str]
    powers: Optional[list]
    weapons: Optional[list]
    damage: Optional[dict]
    ammo: Optional[int]
    money: Optional[int]
    encounters: Optional[list]

    class Config:
        orm_mode = True


class ShowEncounterMonster(BaseModel):
    id: Optional[int]
    monster_name: Optional[str]
    charisma: Optional[int]
    pace: Optional[int]
    parry: Optional[int]
    toughness: Optional[int]
    attributes: Optional[dict]
    skills: Optional[dict]
    gear: Optional[list]
    hindrances: Optional[str]
    edges: Optional[str]
    powers: Optional[list]
    weapons: Optional[list]
    damage: Optional[dict]
    ammo: Optional[int]
    money: Optional[int]
    encounters: Optional[list]

    class Config:
        orm_mode = True
