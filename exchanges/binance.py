#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
from .base.exchange import *
from .errors import *

BINANCE_REST_URL = 'api.binance.com'


class Binance(Exchange):
    @http_exception
    def markets(self):
        MARKETS_RESOURCE = "/api/v1/ticker/allPrices"
        json = self.httpGet(BINANCE_REST_URL,
                            MARKETS_RESOURCE, {}, self._apikey, {})
        return tuple([j["symbol"] for j in json])

    def ticker(self, item='BTCUSDT'):
        TICKER_RESOURCE = "/api/v1/klines"
        params = {
            'symbol': item,
            'iterval': '1d',
        }
        json = self.httpGet(BINANCE_REST_URL, TICKER_RESOURCE,
                            params, self._apikey, params)
        return Ticker(
            timestamp=float(json[-1][0]),
            last=float(json[-1][4]),
            high=float(json[-1][2]),
            low=float(json[-1][3]),
            bid=None,
            ask=None,
            volume=float(json[-1][5])
        )

    def board(self, item=''):
        print("not implemented")

    def order(self, item, order_type, side, price, size, *args, **kwargs):
        print("not implemented")

    def balance(self):
        print("not implemented")
