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
    def __init__(self, apikey, secretkey):
        super().__init__(apikey, secretkey)
        self.session = requests.session()
        self.session.auth = (self._apikey, self._secretkey)

    def markets(self):
        MARKETS_RESOURCE = "/api/2/public/symbol"
        json = self.session.get('https://' + HITBTC_REST_URL +
                                MARKETS_RESOURCE).json()
        return tuple([j["id"] for j in json])

    def ticker(self, item='BTCUSD'):
        TICKER_RESOURCE = "/api/2/public/ticker/" + item
        json = self.session.get('https://' + HITBTC_REST_URL +
                                TICKER_RESOURCE).json()
        return Ticker(
            timestamp=json["timestamp"],
            last=float(json["last"]),
            high=float(json["high"]),
            low=float(json["low"]),
            bid=float(json["bid"]),
            ask=float(json["ask"]),
            volume=float(json["volume"])
        )

    def board(self, item='BTCUSD'):
        BOARD_RESOURCE = "/api/2/public/orderbook/" + item
        json = self.session.get('https://' + HITBTC_REST_URL +
                                BOARD_RESOURCE).json()
        return Board(
            asks=[Ask(price=float(ask["price"]), size=float(ask["size"]))
                  for ask in json["ask"]],
            bids=[Bid(price=float(bid["price"]), size=float(bid["size"]))
                  for bid in json["bid"]],
            mid_price=(float(json["ask"][0]["price"]) + float(json["bid"][0]["price"])) / 2)

    def order(self, item, order_type, side, price, size, *args, **kwargs):
        ORDER_RESOURCE = "/api/2/order"

        params = {
            "symbol": item.lower(),
            "side": side.lower(),
            "quantity": size,
            "price": price
        }
        if order_type != "" and order_type.lower() != "limit":
            params['type'] = order_type.lower()
            params.pop('price')
        json = self.session.post('https://' + HITBTC_REST_URL +
                                 ORDER_RESOURCE, data=params).json()
        return json["clientOrderId"]

    def balance(self):
        BALANCE_RESOURCE = "/api/2/trading/balance"

        session = requests.session()
        session.auth = (self._apikey, self._secretkey)
        json = self.session.get('https://' + HITBTC_REST_URL +
                                BALANCE_RESOURCE).json()

        balances = {}
        for j in json:
            al = float(j["available"]) + float(j["reserved"])
            balances[j['currency']] = [al, float(j["available"])]
        return balances
