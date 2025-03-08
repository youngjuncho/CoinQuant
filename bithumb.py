import asyncio
import httpx
import pandas as pd

class Bithumb:
    _BASE_URL = "https://api.bithumb.com/public"

    def __init__(self):
        self._client = httpx.AsyncClient(base_url=self._BASE_URL, timeout=10.0)

    async def close(self):
        await self._client.aclose()

    async def calculate(self, top20_coins):
        coins = await self._get_coins()
        top20 = [coin for coin in coins if coin in top20_coins]
        btc_price, sma_120days, top3_for_7days, top3_for_3days = await asyncio.gather(
            self._get_btc_price(),
            self._get_sma_120days(),
            self._calculate(top20, 7),
            self._calculate(top20, 3)
        )
        return btc_price, sma_120days, top3_for_7days, top3_for_3days

    async def _get_coins(self):
        url = "/ticker/ALL_KRW"
        response = await self._client.get(url)
        tickers = response.json()
        if tickers['status'] != '0000':
            raise Exception("Failed to fetch ticker from Bithumb")

        return [coin for coin in tickers['data'] if coin != "date"]

    async def _get_btc_price(self):
        url = "/ticker/BTC_KRW"
        response = await self._client.get(url)
        btc = response.json()
        if btc['status'] != '0000':
            raise Exception("Failed to fetch btc from Bithumb")

        return btc['data']['closing_price']

    async def _get_sma_120days(self):
        url = "/candlestick/BTC_KRW/24h"
        response = await self._client.get(url)
        btc_candle_stick = response.json()
        if btc_candle_stick['status'] != '0000':
            raise Exception("Failed to fetch btc candle stick from Bithumb")

        prices = [float(candle[2]) for candle in btc_candle_stick['data']][-120:]
        return pd.DataFrame(prices, columns=['price'])['price'].mean()

    async def _calculate(self, top20, days):
        gainers = []

        for coin in top20:
            await asyncio.sleep(0.2)
            old, current = await self._get_prices(coin, days)
            if old is None or current is None: continue

            gain = ((current - old) / old) * 100
            if gain <= 0: continue

            gainers.append({"coin": coin, "gain": gain})

        return [gainer['coin'] for gainer in sorted(gainers, key=lambda x: x['gain'], reverse=True)[:3]]

    async def _get_prices(self, coin, days):
        url = f"/candlestick/{coin}_KRW/24h"
        response = await self._client.get(url)
        candle_stick = response.json()
        if candle_stick['status'] != '0000' or not candle_stick['data']:
            return None, None

        prices = [candle[2] for candle in candle_stick['data'][-days:]]
        if len(prices) != days:
            return None, None

        return float(prices[0]), float(prices[-1])
