import time
import pandas as pd
import requests

class Upbit:
    def __init__(self, top20_coins):
        self._top20_coins = [coin for coin in self._get_coins() if coin[4:] in top20_coins]

    def _get_coins(self):
        url = "https://api.upbit.com/v1/market/all"
        response = requests.get(url)
        return [market['market'] for market in response.json() if market['market'].startswith("KRW-")]

    def get_btc_price(self):
        url = "https://api.upbit.com/v1/ticker"
        params = {
            "markets": "KRW-BTC"
        }
        response = requests.get(url, params=params)
        return float(response.json()[0]['trade_price'])

    def get_120_day_sma(self):
        url = "https://api.upbit.com/v1/candles/days"
        params = {
            "market": "KRW-BTC",
            "count": 200
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception("Failed to fetch btc candles from Upbit")
        
        prices = [float(candle['trade_price']) for candle in response.json()]
        return pd.DataFrame(prices, columns=['price'])['price'].mean()

    def calculate(self, days):
        gainers = []

        for coin in self._top20_coins:
            time.sleep(0.1)
            old, current = self._get_prices(coin, days)
            if (old is None or current is None): continue

            gain = ((current - old) / old) * 100
            if (gain <= 0): continue

            gainers.append({"coin": coin, "gain": gain})

        return [gainer['coin'][4:] for gainer in sorted(gainers, key=lambda x: x['gain'], reverse=True)[:3]]

    def _get_prices(self, coin, days):
        url = "https://api.upbit.com/v1/candles/days"
        params = {
            "market": coin,
            "count": days
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return None, None

        candles = response.json()
        if len(candles) < days:
            return None, None

        return float(candles[-1]['trade_price']), float(candles[1]['trade_price'])
