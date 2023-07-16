from pydantic import BaseModel


class GearInput(BaseModel):
    user_id: int
    character_name: str
    gear_name: str
    amount: int


class WeaponInput(BaseModel):
    user_id: int
    character_name: str
    weapon_name: str
    amount: int
