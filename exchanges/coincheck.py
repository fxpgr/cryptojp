#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from tools.HttpHMACUtil import buildMySign,httpGet,httpPost,getnonce
from .base.exchange import *
import time

COINCHECK_REST_URL = 'coincheck.jp'

class Coincheck(Exchange):
    def markets(self):
        return ("btc_jpy",)

    def ticker(self,item = ''):
        TICKER_RESOURCE = "/api/ticker"
        params = {}
        sign = buildMySign(params,self._secretkey,COINCHECK_REST_URL+TICKER_RESOURCE)
        json = httpGet(COINCHECK_REST_URL,TICKER_RESOURCE,params,self._apikey,sign)

        return Ticker(
            timestamp = int(json["timestamp"]),
            last = float(json["last"]),
            bid = float(json["bid"]),
            ask = float(json["ask"]),
            high = float(json["high"]),
            low = float(json["low"]),
            volume = float(json["volume"])
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
