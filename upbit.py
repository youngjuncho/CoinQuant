import asyncio
import httpx
import pandas as pd

class Upbit:
    _BASE_URL = "https://api.upbit.com/v1"

    def __init__(self):
        self._client = httpx.AsyncClient(base_url=self._BASE_URL, timeout=10.0)

    async def close(self):
        await self._client.aclose()

    async def calculate(self, top20_coins):
        coins = await self._get_coins()
        top20 = [coin for coin in coins if coin[4:] in top20_coins]
        btc_price, sma_120days, top3_for_7days, top3_for_3days = await asyncio.gather(
            self._get_btc_price(),
            self._get_sma_120days(),
            self._calculate(top20, 7),
            self._calculate(top20, 3)
        )
        return btc_price, sma_120days, top3_for_7days, top3_for_3days

    async def _get_coins(self):
        url = "/market/all"
        response = await self._client.get(url)
        return [market['market'] for market in response.json() if market['market'].startswith("KRW-")]

    async def _get_btc_price(self):
        url = "/ticker"
        params = {
            "markets": "KRW-BTC"
        }
        response = await self._client.get(url, params=params)
        return float(response.json()[0]['trade_price'])

    async def _get_sma_120days(self):
        url = "/candles/days"
        params = {
            "market": "KRW-BTC",
            "count": 200
        }
        response = await self._client.get(url, params=params)
        if response.status_code != 200:
            raise Exception("Failed to fetch btc candles from Upbit")
        
        prices = [float(candle['trade_price']) for candle in response.json()]
        return pd.DataFrame(prices, columns=['price'])['price'].mean()

    async def _calculate(self, top20, days):
        gainers = []

        for coin in top20:
            await asyncio.sleep(0.1)
            old, current = await self._get_prices(coin, days)
            if old is None or current is None: continue

            gain = ((current - old) / old) * 100
            if gain <= 0: continue

            gainers.append({"coin": coin, "gain": gain})

        return [gainer['coin'][4:] for gainer in sorted(gainers, key=lambda x: x['gain'], reverse=True)[:3]]

    async def _get_prices(self, coin, days):
        url = "/candles/days"
        params = {
            "market": coin,
            "count": days
        }
        response = await self._client.get(url, params=params)
        if response.status_code != 200:
            return None, None

        candles = response.json()
        if len(candles) < days:
            return None, None

        return float(candles[-1]['trade_price']), float(candles[1]['trade_price'])
