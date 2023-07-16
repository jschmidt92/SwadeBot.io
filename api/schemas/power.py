from pydantic import BaseModel, Field
from typing import Optional


class PowerCreate(BaseModel):
    name: Optional[str] = Field(...)
    pp: Optional[str] = Field(...)
    range: Optional[str] = Field(...)
    duration: Optional[str] = Field(...)
    effect: Optional[str] = Field(...)
    notes: Optional[str] = Field(...)


class UpdatePower(BaseModel):
    name: Optional[str]
    pp: Optional[str]
    range: Optional[str]
    duration: Optional[str]
    effect: Optional[str]
    notes: Optional[str]


class ShowPower(BaseModel):
    name: str
    pp: str
    range: str
    duration: str
    effect: str
    notes: str

    class Config:
        orm_mode = True
