from pydantic import BaseModel, Field
from typing import Optional


class UserCreate(BaseModel):
    username: Optional[str] = Field(...)
    discord_id: Optional[str] = Field(...)


class UpdateUser(BaseModel):
    username: Optional[str]
    discord_id: Optional[str]


class ShowUser(BaseModel):
    username: Optional[str]
    discord_id: Optional[str]

    class Config:
        orm_mode = True
