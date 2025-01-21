from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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


class Account(BaseModel):
    username: str
    password: str


@app.get("/")
def read_root():
    return {"message": "Hello, World"}


@app.post("/create_account/")
async def create_account(account: Account):
    print(account)
    return {"username": account.username}
