from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query

from sqlmodel import select
from sql_engine import create_db_and_tables, SessionDep
from account.model import Account

app = FastAPI()


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


@app.post("/create_account/")
async def create_account(account: Account, session: SessionDep):
    print(account)
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@app.get("/user/")
async def all_user(
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
