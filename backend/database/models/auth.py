from datetime import datetime

from backend.database.config import Base

from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Text, DateTime, Date, Boolean, Column, ForeignKey


class User(Base):
    __tablename__ = 'user'

    # Table fields
    pk = Column(Integer, primary_key=True)
    first_name = Column(String(256))
    last_name = Column(String(256))
    email = Column(String(256), unique=True)
    password = Column(String(256))
    is_active = Column(Boolean, default=False)

    bank_account = relationship('BankAccount', back_populates='owner')
