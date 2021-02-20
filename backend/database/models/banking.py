from datetime import datetime

from backend.database.config import Base

from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Text, DateTime, Date, Boolean, Column, ForeignKey


class BankAccount(Base):
    __tablename__ = 'bank_account'

    # Table fields
    pk = Column(Integer, primary_key=True)
    api_key = Column(String(512))
    user_pk = Column(Integer, ForeignKey('user.pk'))

    cards = relationship("Card")
    owner = relationship('User', back_populates='bank_account')


class Card(Base):
    __tablename__ = 'card'

    # Table fields
    pk = Column(Integer, primary_key=True)
    name = Column(String(256), default="NewCard")
    balance = Column(Integer)
    is_blocked = Column(Boolean, default=False)
    limit = Column(Integer, default=50)
    currency = Column(String(3))

    owner_pk = Column(Integer, ForeignKey("bank_account.pk"))
