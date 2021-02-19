from pydantic import BaseModel

import backend.database.schemas.banking as schemas


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    pk: int
    is_active: bool
    bank_account: schemas.BankingAccount

    class Config:
        orm_mode = True
