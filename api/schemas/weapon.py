from pydantic import BaseModel, Field
from typing import Optional


class WeaponCreate(BaseModel):
    name: Optional[str] = Field(...)
    range: Optional[str] = Field(...)
    damage: Optional[str] = Field(...)
    rof: Optional[int] = Field(...)
    shots: Optional[int] = Field(...)
    min_str: Optional[str] = Field(...)
    wt: Optional[int] = Field(...)
    cost: Optional[int] = Field(...)
    notes: Optional[str] = Field(...)


class UpdateWeapon(BaseModel):
    name: Optional[str]
    range: Optional[str]
    damage: Optional[str]
    rof: Optional[int]
    shots: Optional[int]
    min_str: Optional[str]
    wt: Optional[int]
    cost: Optional[int]
    notes: Optional[str]


class ShowWeapon(BaseModel):
    name: Optional[str]
    range: Optional[str]
    damage: Optional[str]
    rof: Optional[int]
    shots: Optional[int]
    min_str: Optional[str]
    wt: Optional[int]
    cost: Optional[int]
    notes: Optional[str]

    class Config:
        orm_mode = True
