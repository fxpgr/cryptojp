#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from tools.HttpHMACUtil import buildMySign,httpGet,httpPost,getnonce
from settings import *
import time

class Spot():
    def __init__(self):
        self._url = quoineRESTURL
        self._apikey = quoineapikey
        self._secretkey = quoinesecretkey

    def ticker(self,pair = 'BTCUSD'):
        TICKER_RESOURCE = "/products/code/CASH/%s"%(pair)
        params = {}
        sign = buildMySign(params,self._secretkey,self._url+TICKER_RESOURCE)
        json = httpGet(self._url,TICKER_RESOURCE,params,self._apikey,sign)

        self.rate = float(json["last_traded_price"])
        self.ask = float(json["market_ask"])
        self.bid = float(json["market_bid"])
        self.high = float(json["high_market_ask"])
        self.low = float(json["low_market_bid"])
        self.vol = float(json["volume_24h"])

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
