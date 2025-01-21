from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlmodel import select
from sql_engine import create_db_and_tables, SessionDep
from account.model import Account

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


@app.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
):
    statement = select(Account).where(Account.username == form_data.username)
    user_dict = session.exec(statement).first()
    print(user_dict, form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user_password = user_dict.password
    print(user_password, " ", form_data.password)
    if not user_password == form_data.password:
        raise HTTPException(status_code=400, detail="Inccord username or password")
    return {"access_token": user_dict.username, "token_type": "bearer"}


@app.post("/create_account/")
async def create_account(account: Account, session: SessionDep):
    print(account)
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
