from datetime import datetime, timedelta, timezone

from config import get_settings
import jwt
from typing import Annotated
from fastapi import HTTPException, APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel
from passlib.context import CryptContext

from sqlmodel import select
from sql_engine import SessionDep
from account.model import Account

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    settings = get_settings()
    secret_key = settings.SECRET_KEY
    algo_key = settings.ALGORITHM
    return jwt.encode(to_encode, secret_key, algorithm=algo_key)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_hash_password(password: str):
    return pwd_context.hash(password)


def get_user_from_db(username: str, session: SessionDep) -> Account:
    statement = select(Account).where(Account.username == username)
    return session.exec(statement).first()


def authenticate_user(
    username: str, password: str, session: SessionDep
) -> Account | bool:
    user_dict = get_user_from_db(username, session)
    if not user_dict:
        return False
    if not verify_password(password, user_dict.password):
        return False
    return user_dict


@router.post("/token/", tags=["authentication"])
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
):
    user_dict = authenticate_user(form_data.username, form_data.password, session)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    settings = get_settings()
    expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    access_token_expires = timedelta(minutes=expire_minutes)
    access_token = create_access_token(
        data={"sub": user_dict.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
