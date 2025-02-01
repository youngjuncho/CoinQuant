import asyncio

from bithumb import Bithumb
from coingecko import Coingecko
from coinmarketcap import Coinmarketcap
from upbit import Upbit

async def coinmarketcap():
    coinmarketcap = Coinmarketcap()
    top20_coins = await coinmarketcap.calculate()
    await coinmarketcap.close()
    print(f"Coinmarketcap : Top 20 : {top20_coins}\n")
    return top20_coins

async def coingecko():
    coingecko = Coingecko()
    btc_price, sma_120days = await coingecko.calculate()
    await coingecko.close()
    print(f"Coingecko : BTC price : {btc_price}")
    print(f"Coingecko : 120 day SMA : {sma_120days}\n")

async def bithumb(top20_coins):
    bithumb = Bithumb()
    btc_price, sma_120days, top3_for_7days, top3_for_3days = await bithumb.calculate(top20_coins)
    await bithumb.close()
    print(f"Bithumb : BTC price : {btc_price}")
    print(f"Bithumb : 120 day SMA : {sma_120days}")
    print(f"Bithumb[7] : {top3_for_7days}")
    print(f"Bithumb[3] : {top3_for_3days}\n")

# upbit = Upbit(top20_coins)
# print(f"Upbit : BTC price : {upbit.get_btc_price()}")
# print(f"Upbit : 120 day SMA : {upbit.get_120_day_sma()}")
# print(f"Upbit[7] : {upbit.calculate(7)}")
# print(f"Upbit[3] : {upbit.calculate(3)}")

async def main():
    top20_coins = await coinmarketcap()
    await coingecko()
    await bithumb(top20_coins)

asyncio.run(main())
