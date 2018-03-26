#!/usr/bin/python
# -*- coding: utf-8 -*-
from .base.exchange import *
import time
import requests
from datetime import datetime
import calendar
import jwt

QUOINE_REST_URL = 'api.quoine.com'


class Quoine(Exchange):
    def __init__(self, apikey, secretkey):
        def httpGet(url, resource, params, apikey, sign):
            payload = {'nonce': str(int("{:.6f}".format(
                time.time()).replace('.', ''))), 'path': resource, 'token_id': self._apikey}
            headers = {
                'Accept': 'application/json',
                'X-Quoine-API-Version': '2',
                "X-Quoine-Auth": apikey,
                "Sign": jwt.encode(payload, self._secretkey, 'HS256'),
            }
            return self.session.get('https://' + url + resource,
                                    headers=headers, data=params).json()

        def httpPost(url, resource, params, apikey):
            payload = {'nonce': str(int("{:.6f}".format(
                time.time()).replace('.', ''))), 'path': resource, 'token_id': self._apikey}
            headers = {
                'Accept': 'application/json',
                'X-Quoine-API-Version': '2',
                "X-Quoine-Auth": apikey,
                "Sign": jwt.encode(payload, self._secretkey, 'HS256'),
            }
            return self.session.post('https://' + url + resource,
                                     headers=headers, data=params).json()

        def httpPut(url, resource, params, apikey):
            payload = {'nonce': str(int("{:.6f}".format(
                time.time()).replace('.', ''))), 'path': resource, 'token_id': self._apikey}
            headers = {
                'Accept': 'application/json',
                'X-Quoine-API-Version': '2',
                "X-Quoine-Auth": apikey,
                "Sign": jwt.encode(payload, self._secretkey, 'HS256'),
            }
            return self.session.put('https://' + url + resource, headers=headers, data=params).json()
        super(Quoine, self).__init__(apikey, secretkey)
        self.session = requests.session()
        self.httpPost = httpPost
        self.httpGet = httpGet
        self.httpPut = httpPut

    def __del__(self):
        self.session.close()

    def markets(self):
        MARKETS_RESOURCE = "/products"
        json = self.session.get('https://' + QUOINE_REST_URL +
                                MARKETS_RESOURCE).json()
        li = [[j['id'], j['currency_pair_code']] for j in json]
        self.market_dict = dict(li)
        return tuple([CurrencyPair(trading=j['base_currency'], settlement=j["quoted_currency"]) for j in json])

    def ticker(self, trading, settlement):
        TICKER_RESOURCE = "/products/code/CASH/%s" % (trading + settlement)
        json = self.session.get('https://' + QUOINE_REST_URL +
                                TICKER_RESOURCE).json()

        utc = datetime.utcfromtimestamp(time.time())
        return Ticker(
            timestamp=calendar.timegm(utc.timetuple()),
            last=float(json["last_traded_price"]),
            ask=float(json["market_ask"]),
            bid=float(json["market_bid"]),
            high=float(json["high_market_ask"]),
            low=float(json["low_market_bid"]),
            volume=float(json["volume_24h"]),
        )

    def board(self, item='BTCUSD'):
        if not self.market_dict:
            self.markets()
        product_id = tuple(self.market_dict.keys())[
            tuple(self.market_dict.values()).index(item)]
        BOARD_RESOURCE = "/products/%s/price_levels" % product_id
        json = self.session.get('https://' + QUOINE_REST_URL +
                                BOARD_RESOURCE).json()
        return Board(
            asks=[Ask(price=float(ask[0]), size=float(ask[1]))
                  for ask in json["buy_price_levels"]],
            bids=[Bid(price=float(bid[0]), size=float(bid[1]))
                  for bid in json["sell_price_levels"]],
            mid_price=(float(json["buy_price_levels"][0][0]) +
                       float(json["sell_price_levels"][0][0])) / 2
        )

    def balance(self):
        BALANCE_RESOURCE = "/accounts/balance"
        params = {
        }
        json = self.httpGet(QUOINE_REST_URL,
                            BALANCE_RESOURCE, params, self._apikey, self._secretkey)

        balances = {}
        for j in json:
            balances[j['currency']] = [
                float(j["balance"]), float(j["balance"])]
        return balances

    def order(self, trading, settlement, order_type, side, price, size):
        ORDER_RESOURCE = "/orders"
        params = {
            "order_type": order_type.lower(),
            "product_id": trading + settlement,
            "side": side.lower(),
            "price": price,
            "quantity": size
        }
        json = self.httpPost(QUOINE_REST_URL,
                             ORDER_RESOURCE, params, self._apikey)
        return json["id"]

    def get_open_orders(self, symbol="BTC_JPY"):
        OPEN_ORDERS_RESOURCE = "/orders"
        params = {"status": "live"}
        json = self.httpGet(QUOINE_REST_URL,
                            OPEN_ORDERS_RESOURCE, params, self._apikey, self._secretkey)
        return json

    def cancel_order(self, symbol, order_id):
        CANCEL_ORDERS_RESOURCE = "/orders/{0}/cancel".format(order_id)
        self.httpPost(QUOINE_REST_URL, CANCEL_ORDERS_RESOURCE, {}, self._apikey, self._secretkey)

    def get_fee(self, symbol="BTC_JPY"):
        GET_FEE_RESOURCE = "/products"

        json = self.httpGet(QUOINE_REST_URL, GET_FEE_RESOURCE, {}, self._apikey, self._secretkey)
        res = []
        for j in json:
            if j["currency_pair_code"] == symbol:
                res = [j["taker_fee"], j["maker_fee"]]
                break
        return res
