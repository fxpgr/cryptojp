#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
from .base.exchange import *
from .errors import *
import requests

HITBTC_REST_URL = 'api.hitbtc.com'


class Hitbtc(Exchange):
    def markets(self):
        MARKETS_RESOURCE = "/api/2/public/symbol"
        json = self.httpGet(HITBTC_REST_URL,
                            MARKETS_RESOURCE, {}, self._apikey, {})
        return tuple([j["id"] for j in json])

    def ticker(self, item='BTCUSD'):
        TICKER_RESOURCE = "/api/2/public/ticker/" + item
        json = self.httpGet(HITBTC_REST_URL, TICKER_RESOURCE,
                            {}, self._apikey, {})
        return Ticker(
            timestamp=json["timestamp"],
            last=float(json["last"]),
            high=float(json["high"]),
            low=float(json["low"]),
            bid=float(json["bid"]),
            ask=float(json["ask"]),
            volume=float(json["volume"])
        )

    def board(self, item=''):
        print("not implemented!")

    def order(self, item, order_type, side, price, size, *args, **kwargs):
        ORDER_RESOURCE = "/api/2/order"

        session = requests.session()
        session.auth = (self._apikey, self._secretkey)

        params = {
            "symbol": item.lower(),
            "side": side.lower(),
            "quantity": size,
            "price": price
        }
        json = session.post('https://' + HITBTC_REST_URL +
                            ORDER_RESOURCE, data=params).json()
        return json["clientOrderId"]

    def balance(self):
        BALANCE_RESOURCE = "/api/2/trading/balance"

        session = requests.session()
        session.auth = (self._apikey, self._secretkey)
        json = session.get('https://' + HITBTC_REST_URL +
                           BALANCE_RESOURCE).json()

        balances = {}
        for j in json:
            balances[j['currency']] = [
                float(j["available"]) + float(j["reserved"]), float(j["available"])]
        return balances
