from exchanges import bitflyer
from exchanges import coincheck
from exchanges import zaif
from exchanges import btcbox

def NewExchange(exchange_name,apikey,secretkey):
    if exchange_name == "bitflyer":
        return bitflyer.Bitflyer(apikey,secretkey)
    elif exchange_name == "coincheck":
        return coincheck.Coincheck(apikey,secretkey)
    elif exchange_name == "zaif":
        return zaif.Zaif(apikey,secretkey)
    elif exchange_name == "btcbox":
        return btcbox.Btcbox(apikey,secretkey)
    raise ValueError("error!")

EXCHANGES = (
"bitflyer",
"coincheck",
"zaif",
"btcbox"
)
