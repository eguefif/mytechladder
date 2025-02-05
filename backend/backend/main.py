from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from sql_engine import create_db_and_tables
from account import controllers as users
import authentication

app = FastAPI()

app.include_router(users.router)
app.include_router(authentication.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


origins = [
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
