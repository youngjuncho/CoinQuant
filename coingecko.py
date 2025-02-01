import asyncio
import httpx
import pandas as pd

class Coingecko:
    _BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self):
        self._client = httpx.AsyncClient(base_url=self._BASE_URL, timeout=10.0)

    async def close(self):
        await self._client.aclose()

    async def calculate(self):
        btc_price, sma_120days = await asyncio.gather(self._get_btc_price(), self._get_sma_120days())
        return btc_price, sma_120days

    async def _get_btc_price(self):
        url = "/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd",
        }

        response = await self._client.get(url, params=params)
        if response.status_code != 200:
            raise Exception("Failed to fetch current BTC price.")

        return response.json()["bitcoin"]["usd"]

    async def _get_sma_120days(self):
        url = "/coins/bitcoin/market_chart"
        params = {
            "vs_currency": "usd",
            "days": "120",
        }

        response = await self._client.get(url, params=params)
        if response.status_code != 200:
            raise Exception("Failed to fetch BTC historical data.")

        prices = [price[1] for price in response.json()['prices']]
        return pd.DataFrame(prices, columns=['price'])['price'].mean()
