import asyncio

from bithumb import Bithumb
from coingecko import Coingecko
from coinmarketcap import Coinmarketcap
from upbit import Upbit

top20_coins = []

async def coinmarketcap():
    coinmarketcap = Coinmarketcap()
    top20_coins = await coinmarketcap.get_top20_coins()
    await coinmarketcap.close()
    print(f"Coinmarketcap : Top 20 : {top20_coins}\n")

async def coingecko():
    coingecko = Coingecko()
    btc_price, sma_120_days = await coingecko.get_btc_price_sma_120_days()
    await coingecko.close()
    print(f"Coingecko : BTC price : {btc_price}")
    print(f"Coingecko : 120 day SMA : {sma_120_days}\n")

# bithumb = Bithumb(top20_coins)
# print(f"Bithumb : BTC price : {bithumb.get_btc_price()}")
# print(f"Bithumb : 120 day SMA : {bithumb.get_120_day_sma()}")
# print(f"Bithumb[7] : {bithumb.calculate(7)}")
# print(f"Bithumb[3] : {bithumb.calculate(3)}\n")
#
# upbit = Upbit(top20_coins)
# print(f"Upbit : BTC price : {upbit.get_btc_price()}")
# print(f"Upbit : 120 day SMA : {upbit.get_120_day_sma()}")
# print(f"Upbit[7] : {upbit.calculate(7)}")
# print(f"Upbit[3] : {upbit.calculate(3)}")

async def main():
    await coinmarketcap()
    await coingecko()

asyncio.run(main())
