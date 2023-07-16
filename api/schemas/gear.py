from pydantic import BaseModel, Field
from typing import Optional


class GearCreate(BaseModel):
    name: Optional[str] = Field(...)
    min_str: Optional[str] = Field(...)
    wt: Optional[int] = Field(...)
    cost: Optional[int] = Field(...)
    notes: Optional[str] = Field(...)


class UpdateGear(BaseModel):
    name: Optional[str]
    min_str: Optional[str]
    wt: Optional[int]
    cost: Optional[int]
    notes: Optional[str]


class ShowGear(BaseModel):
    name: Optional[str]
    min_str: Optional[str]
    wt: Optional[int]
    cost: Optional[int]
    notes: Optional[str]

    class Config:
        orm_mode = True
