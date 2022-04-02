from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from pydantic.types import conint


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    username: str
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class Crypto(BaseModel):  # ADD, Get Signal : request+ responce model
    pair_name: str
    crypto_exchange: str



class Signal(BaseModel):
    name: str
    signal_stage: str
    exchange: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class ListMessage(BaseModel):
    message: list
