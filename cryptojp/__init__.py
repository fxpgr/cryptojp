from . import bitflyer
from . import coincheck
from . import btcbox
from . import kraken
from . import quoine
from . import hitbtc
from . import binance
from . import bitfinex
from . import poloniex
from . import realcurrency


def NewExchange(exchange_name, apikey, secretkey):
    if exchange_name == "bitflyer":
        return bitflyer.Bitflyer(apikey, secretkey)
    elif exchange_name == "coincheck":
        return coincheck.Coincheck(apikey, secretkey)
    elif exchange_name == "btcbox":
        return btcbox.Btcbox(apikey, secretkey)
    elif exchange_name == "kraken":
        return kraken.Kraken(apikey, secretkey)
    elif exchange_name == "quoine":
        return quoine.Quoine(apikey, secretkey)
    elif exchange_name == "hitbtc":
        return hitbtc.Hitbtc(apikey, secretkey)
    elif exchange_name == "binance":
        return binance.Binance(apikey, secretkey)
    elif exchange_name == "poloniex":
        return poloniex.Poloniex(apikey, secretkey)
    elif exchange_name == "bitfinex":
        return bitfinex.Bitfinex(apikey, secretkey)
    elif exchange_name == "realcurrency":
        return realcurrency.RealCurrency(apikey, secretkey)
    print("not implemented")
