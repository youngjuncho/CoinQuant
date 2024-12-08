import requests

class Coinmarketcap:
    _API_KEY = "e868c6fd-3c23-4a12-84ba-afdb128f61f5"
    _BASE_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency"
    _HEADERS = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": _API_KEY
    }

    def __init__(self):
        pass

    def get_top20_coins(self):
        url = f"{self._BASE_URL}/listings/latest"
        params = {
            "start": 1,
            "convert": "USD"
        }
        response = requests.get(url, headers=self._HEADERS, params=params)
        coins = response.json()

        top100 = [coin['symbol'] for coin in coins['data']]
        stables = self._get_stable_coins()
        return [coin for coin in top100 if coin not in stables][:20]

    def _get_stable_coins(self):
        url = f"{self._BASE_URL}/category"
        params = {
            "id": self._get_stable_id()
        }
        response = requests.get(url, headers=self._HEADERS, params=params)
        category = response.json()

        return [coin['symbol'] for coin in category['data'].get('coins')]

    def _get_stable_id(self):
        url = f"{self._BASE_URL}/categories"
        response = requests.get(url, headers=self._HEADERS)
        categories = response.json()

        return [{'id':category['id'], 'name':category['name']} for category in categories['data'] if category['name'] == "Stablecoin"][0].get('id')
