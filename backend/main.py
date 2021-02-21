from typing import List

from datetime import timedelta

from fastapi.security import  OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException, status

from sqlalchemy.orm import Session

from backend import utils
from backend import crud
from backend import dependable

from backend.database.schemas import auth as auth_schemas
from backend.database.schemas import banking as banking_schemas

from backend.database.config import  Base, engine
from backend.utils import oauth2_scheme

Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.post('/', response_model=auth_schemas.User)
def create_user(
        user: auth_schemas.UserCreate,
        db: Session = Depends(dependable.get_db)
):

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already exists')

    user.password = utils.get_password_hashed(user.password)

    user_created = crud.create_user(db, user)

    return user_created


@app.get('/all', response_model=List[auth_schemas.User], dependencies=[Depends(oauth2_scheme)])
def get_users(
        skip: int = 0,
        limit: int = 500,
        db: Session = Depends(dependable.get_db)
):

    users = crud.get_users(db, skip, limit)
    return users


@app.get('/{pk}', response_model=auth_schemas.User, dependencies=[Depends(oauth2_scheme)])
def get_user(
        pk: int,
        db: Session = Depends(dependable.get_db)
):

    user = crud.get_user(db, pk)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@app.post('/bank', response_model=banking_schemas.BankingAccount, dependencies=[Depends(oauth2_scheme)])
def create_banking_account(
        account: banking_schemas.BankingAccountCreate,
        cards: List[banking_schemas.Card],
        owner: auth_schemas.User,
        db: Session = Depends(dependable.get_db)
):
    account = crud.create_banking_account(db, account=account, cards=cards, owner=owner)
    if account:
        raise HTTPException(status_code=400, detail='Banking Account already exists')
    return account


@app.post('/bank/card', response_model=banking_schemas.Card, dependencies=[Depends(oauth2_scheme)])
def create_card(
        card: banking_schemas.CardCreate,
        owner_pk: int,
        db: Session = Depends(dependable.get_db)
):
    card = crud.create_card(db, card=card, owner_pk=owner_pk)
    if card:
        raise HTTPException(status_code=400, detail='Card already exists')
    return card


@app.post('/token', response_model=auth_schemas.Token)
def login_for_access_token(
       form_data: OAuth2PasswordRequestForm = Depends(),
       db: Session = Depends(dependable.get_db)
):
    user = utils.authenticate_user(db=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={'sub': user.email},
        expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get('/me', response_model=auth_schemas.User)
def read_users_me(
    current_user: auth_schemas.User = Depends(utils.get_active_user),
):
    return current_user
