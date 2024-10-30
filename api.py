from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models import Currency
from db import get_session


app = FastAPI()


@app.get("/prices")
async def get_prices(ticker: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Currency).filter(Currency.ticker == ticker))
    return result.mappings().all()


@app.get("/prices/latest")
async def get_latest_price(ticker: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Currency.price).filter(Currency.ticker == ticker).order_by(Currency.timestamp.desc()).limit(1))
    return result.mappings().all()


@app.get("/prices/filter")
async def get_price_by_date(ticker: str, start_date: int, end_date: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Currency.timestamp, Currency.price).filter(Currency.ticker == ticker, Currency.timestamp >= start_date, Currency.timestamp <= end_date))
    return result.mappings().all()