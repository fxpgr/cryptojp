from . import bitflyer
from . import coincheck
from . import btcbox
from . import kraken
from . import quoine
from . import hitbtc


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
    raise ValueError("error!")
