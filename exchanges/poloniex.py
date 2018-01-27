#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
from .base.exchange import *
from .errors import *
import requests
from datetime import datetime
from urllib.parse import urlencode
import time
import calendar
import hmac
import hashlib
import http.client
POLONIEX_REST_URL = 'poloniex.com'


def buildMySign(params, secretKey):
    return hmac.new(secretKey.encode("utf8"), urlencode(params).encode("utf8"), hashlib.sha512).hexdigest()


def getnonce():
    nonce = int("{:.6f}".format(time.time()).replace('.', ''))
    return(nonce)


def httpPost(url, resource, params, apikey, sign, *args, **kwargs):
    params['nonce'] = getnonce()
    headers = {
        "Key": apikey,
        "Sign": buildMySign(params, sign),
    }
    return requests.post('https://' + url + resource,
                         headers=headers, data=params).json()


class Poloniex(Exchange):
    def __init__(self, apikey, secretkey):
        super().__init__(apikey, secretkey)
        self.session = requests.session()
        self.session.auth = (self._apikey, self._secretkey)
        self.httpPost = httpPost

    def markets(self):
        print("not implemented!")

    def ticker(self, item='USDT_BTC'):
        TICKER_RESOURCE = "/public?command=returnTicker"
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
        print("not implemented!")

    def order(self, item, order_type, side, price, size, *args, **kwargs):
        ORDER_RESOURCE = "/tradingApi"

        params = {
            "command": side.lower(),
            "currencyPair": item,
            "rate": str(price),
            "amount": str(size),
        }
        if order_type == "fillOrKill":
            params["fillOrKill"] = "1"
        json = self.httpPost(POLONIEX_REST_URL,
                             ORDER_RESOURCE, params, self._apikey, self._secretkey)
        return json['orderNumber']

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
