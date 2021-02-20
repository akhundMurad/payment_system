from typing import List

from sqlalchemy.orm import Session

from backend.database.schemas import auth as auth_schemas
from backend.database.schemas import banking as banking_schemas

from backend.database.models import auth as auth_models
from backend.database.models import banking as banking_models


def get_user(
        db: Session,
        user_pk: int
):
    """
    Getting user from DB by primary key
    """

    return db.query(auth_models.User).filter(auth_models.User.pk == user_pk).first()


def get_user_by_email(
        db: Session,
        email: str
):
    """
    Getting user from DB by email
    """

    return db.query(auth_models.User).filter(auth_models.User.email == email).first()


def get_users(
        db: Session,
        skip: int = 0,
        limit: int = 500
):
    """
    Getting all users from DB
    """

    return db.query(auth_models.User).offset(skip).limit(limit).all()


def create_user(
        db: Session,
        user: auth_schemas.UserCreate
):
    """
    Creating user
    """

    db_user = auth_models.User(
        **user.dict(),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_card(
        db: Session,
        card: banking_schemas.CardCreate,
        owner_pk: int
):
    """
    Creating visa card
    """

    db_card = banking_models.Card(
        **card.dict(),
        owner_pk=owner_pk
    )

    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def create_banking_account(
        db: Session,
        account: banking_schemas.BankingAccountCreate,
        cards: List[banking_schemas.Card],
        owner: auth_schemas.User
):
    """
    Creating Bank Account for User
    """

    db_account = banking_models.BankAccount(
        **account.dict(),
        cards=cards,
        owner=owner
    )

    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account
