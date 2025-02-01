import asyncio
import httpx

class Coinmarketcap:
    _API_KEY = "e868c6fd-3c23-4a12-84ba-afdb128f61f5"
    _BASE_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency"
    _HEADERS = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": _API_KEY
    }

    def __init__(self):
        self._client = httpx.AsyncClient()

    async def close(self):
        await self._client.aclose()

    def get_top20_coins(self):
        return asyncio.run(self._get_top20_coins())

    async def _get_top20_coins(self):
        url = f"{self._BASE_URL}/listings/latest"
        params = {
            "start": 1,
            "convert": "USD"
        }
        response = await self._client.get(url, headers=self._HEADERS, params=params)
        coins = response.json()

        top100 = [coin['symbol'] for coin in coins['data']]
        stables = await self._get_stable_coins()
        return [coin for coin in top100 if coin not in stables][:20]

    async def _get_stable_coins(self):
        stable_id = await self._get_stable_id()
        if not stable_id:
            return []

        url = f"{self._BASE_URL}/category"
        params = {
            "id": stable_id
        }
        response = await self._client.get(url, headers=self._HEADERS, params=params)
        category = response.json()

        return [coin['symbol'] for coin in category['data'].get('coins')]

    async def _get_stable_id(self):
        url = f"{self._BASE_URL}/categories"
        response = await self._client.get(url, headers=self._HEADERS)
        categories = response.json()

        stable = next((category for category in categories.get('data', []) if category['name'] == "stablecoin"), None)
        return stable['id'] if stable else None
