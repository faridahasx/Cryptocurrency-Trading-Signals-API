from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP,DATE
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String,nullable=False, index=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Crypto(Base):
    __tablename__ = "cryptocurrency"
    name = Column(String, nullable=False)
    exchange = Column(String, nullable=False)
    signal_stage = Column(String, nullable=False)
    id = Column(String, primary_key=True, nullable=False)


class Watchlist(Base):
    __tablename__ = "watchlist"
    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE",onupdate="CASCADE"), primary_key=True)
    crypto_id = Column(String, ForeignKey(
        "cryptocurrency.id", ondelete="CASCADE",onupdate="CASCADE"), primary_key=True)

