import asyncio
import aiohttp
from datetime import datetime

from db import create_db_and_tables, async_session
from models import Currency


async def fetch_price(session, ticker):
    url = f'https://www.deribit.com/api/v2/public/get_index_price?index_name={ticker}'
    async with session.get(url) as response:
        return await response.json()


async def save_to_db(ticker, price):
    record = Currency(ticker=ticker, price=price, timestamp=datetime.now().timestamp())
    async with async_session() as session:
        session.add(record)
        await session.commit()
        await session.refresh(record)


async def get_and_save_prices():
    await create_db_and_tables()
    async with aiohttp.ClientSession() as session:
        while True:
            for ticker in ['btc_usd', 'eth_usd']:
                data = await fetch_price(session, ticker)
                price = data['result']['index_price']
                await save_to_db(ticker, price)
            await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(get_and_save_prices())