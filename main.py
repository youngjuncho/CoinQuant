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

async def upbit(top20_coins):
    upbit = Upbit()
    btc_price, sma_120days, top3_for_7days, top3_for_3days = await upbit.calculate(top20_coins)
    await upbit.close()
    print(f"Upbit : BTC price : {btc_price}")
    print(f"Upbit : 120 day SMA : {sma_120days}")
    print(f"Upbit[7] : {top3_for_7days}")
    print(f"Upbit[3] : {top3_for_3days}\n")

async def main():
    top20_coins = await coinmarketcap()
    await coingecko()
    await bithumb(top20_coins)
    await upbit(top20_coins)

asyncio.run(main())
