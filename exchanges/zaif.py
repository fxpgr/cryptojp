#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
from tools.HttpHMACUtil import buildMySign,httpGet,httpPost,getnonce
from .base.exchange import *
from datetime import datetime
import time,calendar

ZAIF_REST_URL = 'api.zaif.jp'

class Zaif(Exchange):
    def markets(self):
        return ("btc_jpy","xem_jpy","mona_jpy","mona_btc")

    def ticker(self,item = ''):
        TICKER_RESOURCE = "/api/1/ticker/"+item if item != "" else "/api/1/ticker/btc_jpy"
        print(TICKER_RESOURCE)
        params = {}
        json = self.httpGet(ZAIF_REST_URL,TICKER_RESOURCE,params,self._apikey,params)
        utc = datetime.utcfromtimestamp(time.time())
        return Ticker(
            timestamp = calendar.timegm(utc.timetuple()),
            last = float(json["last"]),
            bid = float(json["bid"]),
            ask = float(json["ask"]),
            high = float(json["high"]),
            low = float(json["low"]),
            volume = float(json["volume"])
        )

    def board(self,item = ''):
        BOARD_RESOURCE = "/api/1/depth/"+item if item != "" else "/api/1/depth/btc_jpy"
        params = {}

        json = self.httpGet(ZAIF_REST_URL,BOARD_RESOURCE,params,self._apikey,params)
        return Board(
            asks=[Ask(price=float(ask[0]),size=float(ask[1])) for ask in json["asks"]],
            bids=[Bid(price=float(bid[0]),size=float(bid[1])) for bid in json["bids"]],
            mid_price= (float(json["asks"][0][0])+float(json["bids"][0][0]))/2
        )

    def trades(self,symbol = ''):
        TRADES_RESOURCE = "/api/trades"
        params = {}
        sign = buildMySign(params,self._secretkey,self._url+TRADES_RESOURCE)
        return httpGet(self._url,TRADES_RESOURCE,params,self._apikey,sign)

    def history(self):
        USERINFO_RESOURCE = "/api/exchange/orders/transactions"
        params = {}
        sign = buildMySign(params,self._secretkey,self._url+USERINFO_RESOURCE)
        return httpGet(self._url,USERINFO_RESOURCE,params,self._apikey,sign)

    def ordersinfo(self):
        ORDERS_INFO_RESOURCE = "/api/exchange/orders/opens"
        params = {
         'api_key':self._apikey,
        }
        params['sign'] = buildMySign(params,self._secretkey,self._url+ORDERS_INFO_RESOURCE)
        sign = buildMySign(params,self._secretkey,self._url+ORDERS_INFO_RESOURCE)
        return httpPost(self._url,ORDERS_INFO_RESOURCE,params,self._apikey,sign)

    def trade(self,symbol,tradeType,price='',amount='',limit=''):
        TRADE_RESOURCE = "/api/exchange/orders"
        params = {
            'pair':symbol,
            'order_type':tradeType
        }
        if price:
            params['rate'] = price
        if amount:
            params['amount'] = amount
        sign = buildMySign(params,self._secretkey,self._url+TRADE_RESOURCE)
        return httpPost(self._url,TRADE_RESOURCE,params,self._apikey,sign)

    def balance(self):
        BALANCE_RESOURCE = "/api/accounts/balance"
        params = {}
        sign = buildMySign(params,self._secretkey,self._url+BALANCE_RESOURCE)
        return httpGet(self._url,BALANCE_RESOURCE,params,self._apikey,sign)

    def depth(self):
        DEPTH_RESOURCE = "/api/order_books"
        params = {}
        sign = buildMySign(params,self._secretkey,self._url+DEPTH_RESOURCE)
        return httpGet(self._url,DEPTH_RESOURCE,params,self._apikey,sign)
