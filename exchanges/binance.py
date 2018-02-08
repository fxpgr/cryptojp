#!/usr/bin/python
# -*- coding: utf-8 -*-
from .base.exchange import *
from .errors import *
import requests

BINANCE_REST_URL = 'api.binance.com'


class Binance(Exchange):
    def __init__(self, apikey, secretkey):
        super().__init__(apikey, secretkey)
        self.session = requests.session()

    @http_exception
    def markets(self):
        MARKETS_RESOURCE = "/api/v1/ticker/allBookTickers"
        json = self.session.get('https://' + BINANCE_REST_URL +
                                MARKETS_RESOURCE).json()
        return tuple([j["symbol"] for j in json])

    @http_exception
    def ticker(self, item='BTCUSDT'):
        TICKER_RESOURCE = "/api/v1/klines"
        params = {
            'symbol': item,
            'interval': '1d',
        }
        json = self.session.get('https://' + BINANCE_REST_URL +
                                TICKER_RESOURCE, params=params).json()
        return Ticker(
            timestamp=float(json[-1][0]),
            last=float(json[-1][4]),
            high=float(json[-1][2]),
            low=float(json[-1][3]),
            bid=None,
            ask=None,
            volume=float(json[-1][5])
        )

    @staticmethod
    def board(item=''):
        print("not implemented")

    @staticmethod
    def order(item, order_type, side, price, size):
        print("not implemented")

    @staticmethod
    def balance():
        print("not implemented")
