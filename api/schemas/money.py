from pydantic import BaseModel


class MoneyInput(BaseModel):
    user_id: int
    character_name: str
    amount: int


class MoneyCheck(BaseModel):
    user_id: int
    character_name: str
