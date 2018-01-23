#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
from .base.exchange import *
from .errors import *

BITFLYER_REST_URL = 'api.bitflyer.jp'


class Bitflyer(Exchange):
    @http_exception
    def markets(self):
        MARKETS_RESOURCE = "/v1/markets"
        json = self.httpGet(BITFLYER_REST_URL,
                            MARKETS_RESOURCE, {}, self._apikey, {})
        return tuple([j["product_code"] for j in json])

    def ticker(self, item=''):
        TICKER_RESOURCE = "/v1/ticker"
        params = {}
        if item:
            params["product_code"] = item[0:3] + "_" + item[3:6]
        json = self.httpGet(BITFLYER_REST_URL, TICKER_RESOURCE,
                            params, self._apikey, params)
        return Ticker(
            timestamp=json["timestamp"],
            last=float(json["ltp"]),
            high=None,
            low=None,
            bid=float(json["best_bid"]),
            ask=float(json["best_ask"]),
            volume=float(json["volume"])
        )

    def board(self, item=''):
        BOARD_RESOURCE = "/v1/board"
        params = {}
        json = self.httpGet(BITFLYER_REST_URL, BOARD_RESOURCE,
                            params, self._apikey, params)
        return Board(
            asks=[Ask(price=float(ask["price"]), size=float(ask["size"]))
                  for ask in json["asks"]],
            bids=[Bid(price=float(bid["price"]), size=float(bid["size"]))
                  for bid in json["bids"]],
            mid_price=float(json["mid_price"])
        )

    def order(self, item, order_type, side, price, size, *args, **kwargs):
        ORDER_RESOURCE = "/v1/sendchildorder"
        params = {
            "product_code": item,
            "child_order_type": order_type.upper(),
            "side": side.upper(),
            "price": price,
            "size": size
        }
        if order_type.lower() != "limit":
            params.pop('price')
        sign = self.buildMySign(params, self._secretkey,
                                BITFLYER_REST_URL + ORDER_RESOURCE)
        json = self.httpPost(BITFLYER_REST_URL, ORDER_RESOURCE,
                             params, self._apikey, sign)
        return json["child_order_acceptance_id"]

    def balance(self):
        BALANCE_RESOURCE = "/v1/me/getbalance"
        params = {
        }
        json = self.httpGet(BITFLYER_REST_URL,
                            BALANCE_RESOURCE, {}, self._apikey, {})

        balances = {}
        for j in json:
            balances[j['currency_code']] = [j["amount"], j["available"]]
        return balances
