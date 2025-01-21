from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

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
