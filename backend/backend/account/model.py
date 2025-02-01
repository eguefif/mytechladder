from sqlmodel import Field, SQLModel


class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)


class AccountIn(Account):
    password: str = Field()
