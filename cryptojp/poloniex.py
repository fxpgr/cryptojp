#!/usr/bin/python
# -*- coding: utf-8 -*-
from .base.exchange import *
import requests
from datetime import datetime
import sys
if sys.version_info.major <= 2:
    from urllib import urlencode
else:
    from urllib.parse import urlencode
import time
import calendar
import hmac
import hashlib
POLONIEX_REST_URL = 'poloniex.com'


class Poloniex(Exchange):
    def __init__(self, apikey, secretkey):
        def httpPost(url, resource, params, apikey, sign):
            params['nonce'] = int("{:.6f}".format(
                time.time()).replace('.', ''))
            headers = {
                "Key": apikey,
                "Sign": hmac.new(sign.encode("utf8"), urlencode(params).encode("utf8"), hashlib.sha512).hexdigest(),
            }
            return self.session.post('https://' + url + resource,
                                     headers=headers, data=params).json()
        super(Poloniex, self).__init__(apikey, secretkey)
        self.session = requests.session()
        self.httpPost = httpPost

    def __del__(self):
        self.session.close()

    def markets(self):
        MARKETS_RESOURCE = "/public?command=returnTicker"
        json = self.session.get('https://' + POLONIEX_REST_URL +
                                MARKETS_RESOURCE).json()
        tmp = tuple([j.split("_") for j in json.keys()])
        return [CurrencyPair(trading=t[1], settlement=t[0]) for t in tmp]

    def settlements(self):
        MARKETS_RESOURCE = "/public?command=returnTicker"
        json = self.session.get('https://' + POLONIEX_REST_URL +
                                MARKETS_RESOURCE).json()
        tmp = tuple([j.split("_") for j in json.keys()])
        return tuple(set([t[0] for t in tmp]))

    def settlements(self):
        SETTLEMENTS_RESOURCE = "/public?command=returnTicker"
        js = self.session.get('https://' + POLONIEX_REST_URL +
                              SETTLEMENTS_RESOURCE).json()
        return tuple(set([c.split("_")[0] for c in js.keys()]))

    def ticker(self, trading, settlement):
        TICKER_RESOURCE = "/public?command=returnTicker"
        item = settlement.upper() + "_" + trading.upper()

        json = self.session.get('https://' + POLONIEX_REST_URL +
                                TICKER_RESOURCE).json()
        utc = datetime.utcfromtimestamp(time.time())
        return Ticker(
            timestamp=calendar.timegm(utc.timetuple()),
            last=float(json[item]["last"]),
            high=float(json[item]["high24hr"]),
            low=float(json[item]["low24hr"]),
            bid=float(json[item]["highestBid"]),
            ask=float(json[item]["lowestAsk"]),
            volume=float(json[item]["baseVolume"])
        )

    def board(self, item='USDT_BTC'):
        BOARD_RESOURCE = "/public?command=returnOrderBook&currencyPair=" + item + "&depth=10000"

        json = self.session.get('https://' + POLONIEX_REST_URL +
                                BOARD_RESOURCE).json()
        return Board(
            asks=[Ask(price=float(ask[0]), size=float(ask[1]))
                  for ask in json["asks"]],
            bids=[Bid(price=float(bid[0]), size=float(bid[1]))
                  for bid in json["bids"]],
            mid_price=(float(json["asks"][0][0]) + float(json["bids"][0][0])) / 2
        )

    def order(self, trading, settlement, order_type, side, price, size):
        ORDER_RESOURCE = "/tradingApi"

        params = {
            "command": side.lower(),
            "currencyPair": settlement.upper() + "_" + trading.upper(),
            "rate": str(price),
            "amount": str(size),
        }
        if order_type == "fillOrKill":
            params["fillOrKill"] = "1"
        json = self.httpPost(POLONIEX_REST_URL,
                             ORDER_RESOURCE, params, self._apikey, self._secretkey)
        return json['orderNumber']

    def get_open_orders(self, symbol="USDT_BTC"):
        OPEN_ORDERS_RESOURCE = "/tradingApi"
        params = {
            "command": "returnOpenOrders"
        }
        if symbol:
            params["currencyPair"] = symbol
        json = self.httpPost(POLONIEX_REST_URL,
                             OPEN_ORDERS_RESOURCE, params, self._apikey, self._secretkey)
        return json

    def cancel_order(self, symbol, order_id):
        CANCEL_ORDERS_RESOURCE = "/tradingApi"
        params = {
            "command": "cancelOrder",
            "orderNumber": order_id
        }
        self.httpPost(POLONIEX_REST_URL,
                      CANCEL_ORDERS_RESOURCE, params, self._apikey, self._secretkey)

    def get_fee(self, symbol="BTC_JPY"):
        GET_FEE_RESOURCE = "/tradingApi"
        params = {
            "command": "returnFeeInfo",
        }
        json = self.httpPost(POLONIEX_REST_URL, GET_FEE_RESOURCE, params, self._apikey, self._secretkey)
        return [json["takerFee"], json["makerFee"]]

    def balance(self):
        BALANCE_RESOURCE = "/tradingApi"
        params = {
            "command": "returnCompleteBalances"
        }
        json = self.httpPost(POLONIEX_REST_URL,
                             BALANCE_RESOURCE, params, self._apikey, self._secretkey)
        balances = {}
        for key in sorted(json.keys()):
            balances[key] = [float(json[key]['onOrders']) + float(
                json[key]['available']), float(json[key]['available'])]
        return balances
