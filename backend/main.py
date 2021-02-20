from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from backend import crud

from backend.database.schemas import auth as auth_schemas
from backend.database.schemas import banking as banking_schemas

from backend.database.models import auth as auth_models
from backend.database.models import banking as banking_models

from backend.database.config import SessionLocal, Base, engine


Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/auth/', response_model=auth_schemas.User)
def create_user(
        user: auth_schemas.UserCreate,
        db: Session = Depends(get_db)
):

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already exists')

    user_created = crud.create_user(db, user)

    return user_created


@app.get('/auth/all', response_model=List[auth_schemas.User])
def get_users(
        skip: int = 0,
        limit: int = 500,
        db: Session = Depends(get_db)
):

    users = crud.get_users(db, skip, limit)
    return users


@app.get('/auth/{pk}', response_model=auth_schemas.User)
def get_user(
        pk: int,
        db: Session = Depends(get_db)
):

    user = crud.get_user(db, pk)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@app.post('/auth/bank', response_model=banking_schemas.BankingAccount)
def create_banking_account(
        account: banking_schemas.BankingAccountCreate,
        cards: List[banking_schemas.Card],
        owner: auth_schemas.User,
        db: Session = Depends(get_db)
):
    account = crud.create_banking_account(db, account=account, cards=cards, owner=owner)
    if account:
        raise HTTPException(status_code=400, detail='Banking Account already exists')
    return account


@app.post('/auth/card', response_model=banking_schemas.Card)
def create_card(
        card: banking_schemas.CardCreate,
        owner_pk: int,
        db: Session = Depends(get_db)
):
    card = crud.create_card(db, card=card, owner_pk=owner_pk)
    if card:
        raise HTTPException(status_code=400, detail='Card already exists')
    return card
