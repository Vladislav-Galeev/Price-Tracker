from sqlmodel import SQLModel, Field


class Currency(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    ticker: str
    price: float = Field(ge=0)
    timestamp: int