import pandas as pd
import requests

class Coingecko:
    def __init__(self):
        pass

    def get_btc_price(self):
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd",
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception("Failed to fetch current BTC price.")

        return response.json()["bitcoin"]["usd"]

    def get_120_day_sma(self):
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {
            "vs_currency": "usd",
            "days": "120",
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception("Failed to fetch BTC historical data.")

        prices = [price[1] for price in response.json()['prices']]
        return pd.DataFrame(prices, columns=['price'])['price'].mean()
