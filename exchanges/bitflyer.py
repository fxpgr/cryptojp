#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
from tools.HttpHMACUtil import buildMySign,httpGet,httpPost,getnonce
import time
from .base.exchange import *

BITFLYER_REST_URL = 'api.bitflyer.jp'

class Bitflyer(Exchange):
    def markets(self):
        MARKETS_RESOURCE = "/v1/markets"
        json = httpGet(BITFLYER_REST_URL,MARKETS_RESOURCE,{},self._apikey,{})
        return tuple([j["product_code"] for j in json])

    def ticker(self,item = ''):
        TICKER_RESOURCE = "/v1/ticker"
        params = {}
        if item:
            params["product_code"] = item[0:3]+"_"+item[3:6]
        json = httpGet(BITFLYER_REST_URL,TICKER_RESOURCE,params,self._apikey,params)
        return Ticker(
            timestamp = json["timestamp"],
            last = float(json["ltp"]),
            high = None,
            low = None,
            bid = float(json["best_bid"]),
            ask = float(json["best_ask"]),
            volume = float(json["volume"])
        )

    def trade(self,symbol,tradeType,price='',amount='',*args,**kwargs):
        TRADE_RESOURCE = "/v1/me/sendchildorder"
        symbol = symbol[0:3]+"_"+symbol[3:6]
        tradeType = tradeType.upper()
        symbol = symbol.lower()
        if kwargs["child_order_type"]:child_order_type=kwargs["child_order_type"]
        else:child_order_type="LIMIT"
        params = {
            'product_code':symbol,
            'child_order_type':child_order_type,
            'side':tradeType, # BUY or SELL
            'price':price,
            'size':amount,
            'time_in_force':"FOK"
        }
        sign = buildMySign(params,self._secretkey,self._url+TRADE_RESOURCE)
        try:
            json = httpPost(self._url,TRADES_RESOURCE,params,self._apikey,sign)
            return json['child_order_acceptance_id']
        except:
            return False

    def double_trade(self,symbol,tradeType,prices,amount='',*args,**kwargs):
        TRADE_RESOURCE = "/v1/me/sendparentorder"
        symbol = symbol[0:3]+"_"+symbol[3:6]
        tradeType = tradeType.upper()
        typelist = ["BUY","SELL"]
        if tradeType == "BUY":
            pass
        else:
            typelist.reverse()
        order_params = []
        for t,price in zip(typelist,prices):
            order = {}
            order["product_code"] = symbol.upper()
            order["condition_type"] = "LIMIT"
            order["side"] = tradeType
            order["price"] = price
            order["size"] = amount
            order_params.append(order)

        params = {
            'order_method': "OCO",
            'time_in_force':"FOK",
            'parameters': order_params
        }
        sign = buildMySign(params,self._secretkey,self._url+TRADE_RESOURCE)

    def check_trade(self,i):
        CHECK_ORDER_RESOURCE = "/v1/me/getchildorders"
        params = {
            'product_code':'BTC_JPY',
            'child_order_state':"COMPLETED"
        }
        sign = buildMySign(params,self._secretkey,self._url+CHECK_ORDER_RESOURCE)
        try:
            data = httpPost(self._url,CHECK_ORDER_RESOURCE,params,self._apikey,sign,list_mode=True)
            for d in data:
                if i==d['child_order_acceptance_id']:
                    return True
            return False
        except:
            return False

    def cancel_trade(self,i):
        CHECK_ORDER_RESOURCE = "/v1/me/cancelchildorder"
        params = {
            'product_code':'BTC_JPY',
            'child_order_acceptance_id':i
        }
        sign = buildMySign(params,self._secretkey,self._url+CHECK_ORDER_RESOURCE)
        try:
            data = httpPost(self._url,CHECK_ORDER_RESOURCE,params,self._apikey,sign)
            return True
        except:
            return False


    def ordersinfo(self):
        ORDERS_INFO_RESOURCE = "/api/exchange/orders/opens"
        params = {
         'api_key':self._apikey,
        }
        params['sign'] = buildMySign(params,self._secretkey,self._url+ORDERS_INFO_RESOURCE)
        sign = buildMySign(params,self._secretkey,self._url+ORDERS_INFO_RESOURCE)
        return httpPost(self._url,ORDERS_INFO_RESOURCE,params,self._apikey,sign)


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
