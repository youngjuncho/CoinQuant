import pandas as pd
import requests

class Bithumb:
    def __init__(self, top20_coins):
        self._top20_coins = [coin for coin in self._get_coins() if coin in top20_coins]

    def _get_coins(self):
        url = "https://api.bithumb.com/public/ticker/ALL_KRW"
        response = requests.get(url)
        tickers = response.json()
        if tickers['status'] != '0000':
            raise Exception("Failed to fetch ticker from Bithumb")

        return [coin for coin in tickers['data'] if coin != "date"]

    def get_btc_price(self):
        url = "https://api.bithumb.com/public/ticker/BTC_KRW"
        response = requests.get(url)
        btc = response.json()
        if btc['status'] != '0000':
            raise Exception("Failed to fetch btc from Bithumb")

        return btc['data']['closing_price']
    
    def get_120_day_sma(self):
        url = "https://api.bithumb.com/public/candlestick/BTC_KRW/24h"
        response = requests.get(url)
        btc_candle_stick = response.json()
        if btc_candle_stick['status'] != '0000':
            raise Exception("Failed to fetch btc candle stick from Bithumb")
        
        prices = [float(candle[2]) for candle in btc_candle_stick['data']][-120:]
        return pd.DataFrame(prices, columns=['price'])['price'].mean()

    def calculate(self):
        gainers = []

        for coin in self._top20_coins:
            old, current = self._get_prices(coin)
            if (old is None or current is None): continue

            gain = ((current - old) / old) * 100
            if (gain <= 0): continue

            gainers.append({"coin": coin, "gain": gain})

        return [gainer['coin'] for gainer in sorted(gainers, key=lambda x: x['gain'], reverse=True)[:3]]

    def _get_prices(self, coin):
        url = f"https://api.bithumb.com/public/candlestick/{coin}_KRW/24h"
        response = requests.get(url)
        candle_stick = response.json()
        if candle_stick['status'] != '0000' or not candle_stick['data']:
            return None, None

        prices = [candle[2] for candle in candle_stick['data'][-7:]]
        if len(prices) != 7:
            return None, None

        return float(prices[0]), float(prices[-1])
