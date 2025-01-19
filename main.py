from bithumb import Bithumb
from coingecko import Coingecko
from coinmarketcap import Coinmarketcap
from upbit import Upbit

coinmarketcap = Coinmarketcap()
top20_coins = coinmarketcap.get_top20_coins()
print(f"Coinmarketcap : Top 20 : {top20_coins}\n")

Coingecko = Coingecko()
print(f"Coingecko : BTC price : {Coingecko.get_btc_price()}")
print(f"Coingecko : 120 day SMA : {Coingecko.get_120_day_sma()}\n")

bithumb = Bithumb(top20_coins)
print(f"Bithumb : BTC price : {bithumb.get_btc_price()}")
print(f"Bithumb : 120 day SMA : {bithumb.get_120_day_sma()}")
print(f"Bithumb[7] : {bithumb.calculate(7)}")
print(f"Bithumb[3] : {bithumb.calculate(3)}\n")

upbit = Upbit(top20_coins)
print(f"Upbit : BTC price : {upbit.get_btc_price()}")
print(f"Upbit : 120 day SMA : {upbit.get_120_day_sma()}")
print(f"Upbit[7] : {upbit.calculate(7)}")
print(f"Upbit[3] : {upbit.calculate(3)}")