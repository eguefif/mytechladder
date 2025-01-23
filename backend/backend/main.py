from datetime import datetime, timedelta, timezone
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from passlib.context import CryptContext
import jwt
from sqlmodel import select
from pydantic import BaseModel

from sql_engine import create_db_and_tables, SessionDep
from account.model import Account


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
    print(settings.model_config)
    secret_key = settings.secret_key
    algo_key = settings.algorithm
    return jwt.encode(to_encode, secret_key, algorithm=algo_key)


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


origins = [
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello, World"}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


@app.post("/token")
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
    print(settings.model_config)
    expire_minutes = settings.access_token_expire_minutes
    access_token_expires = timedelta(minutes=expire_minutes)
    access_token = create_access_token(
        data={"sub": user_dict.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.post("/create_account/")
async def create_account(account: Account, session: SessionDep):
    hashed_password = get_hash_password(account.password)
    account.password = hashed_password
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@app.get("/user/")
async def all_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Account]:
    accounts = session.exec(select(Account).offset(offset).limit(limit)).all()
    return accounts


@app.get("/user/")
async def get_user(username: str, session: SessionDep) -> Account:
    user = session.get(Account, username)
    if not user:
        raise HTTPException(status_code=404, detail="User notfound")

    return user
