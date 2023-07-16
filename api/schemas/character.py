from pydantic import BaseModel, Field
from typing import Optional, Union

from db.models.character import Gender, Race


class CharacterCreate(BaseModel):
    user_id: int = Field(...)
    character_name: str = Field(...)
    race: str
    gender: str
    charisma: int = Field(...)
    pace: int = Field(...)
    parry: int = Field(...)
    toughness: int = Field(...)
    attributes: Union[dict, str] = Field(...)
    skills: Union[dict, str] = Field(...)
    gear: Optional[Union[list, str]] = Field(default=[])
    hindrances: str = Field(...)
    edges: str = Field(...)
    powers: Optional[Union[list, str]] = Field(default=[])
    weapons: Optional[Union[list, str]] = Field(default=[])
    damage: Union[dict, str] = Field(...)
    ammo: int = Field(...)
    money: int = Field(...)


class UpdateCharacter(BaseModel):
    user_id: Optional[int]
    character_name: Optional[str]
    race: Optional[Race]
    gender: Optional[Gender]
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


class ShowCharacter(BaseModel):
    id: Optional[int]
    character_name: Optional[str]
    race: Optional[Race]
    gender: Optional[Gender]
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
