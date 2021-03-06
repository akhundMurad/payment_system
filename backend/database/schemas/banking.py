from pydantic import BaseModel
from typing import List

from backend.database.schemas.auth import User


class CardBase(BaseModel):
    name: str
    balance: int
    currency: str


class BankingAccountBase(BaseModel):
    api_key: str


class CardCreate(CardBase):
    is_blocked: bool
    limit: int


class BankingAccountCreate(BankingAccountBase):
    owner: User


class Card(CardBase):
    pk: int
    owner: int

    class Config:
        orm_mode = True


class BankingAccount(BankingAccountBase):
    pk: int
    is_active: bool
    owner: User
    cards: List[Card]

    class Config:
        orm_mode = True
