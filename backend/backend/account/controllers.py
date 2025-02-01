from typing import Annotated
from fastapi import APIRouter, Depends, Query, HTTPException

from sqlmodel import select

from sql_engine import SessionDep
from account.model import Account, AccountIn

from authentication import get_hash_password, oauth2_scheme


router = APIRouter()


@router.post("/create_account/", tags=["users"])
async def create_account(account: AccountIn, session: SessionDep) -> Account:
    hashed_password = get_hash_password(account.password)
    account.password = hashed_password
    session.add(account)
    session.commit()
    session.refresh(account)
    return account


@router.get("/users/", tags=["users"])
async def all_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Account]:
    accounts = session.exec(select(Account).offset(offset).limit(limit)).all()
    return accounts


@router.get("/user/{user}", tags=["users"])
async def get_user(user: str, session: SessionDep) -> Account:
    user = session.exec(select(Account).where(Account.username == user))
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User notfound")

    return user.one()
