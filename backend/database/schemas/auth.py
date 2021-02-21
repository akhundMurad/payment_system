from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    pk: int
    is_active: bool

    class Config:
        orm_mode = True


class UserInDB(UserCreate, User):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(Token):
    username: Optional[str] = None
