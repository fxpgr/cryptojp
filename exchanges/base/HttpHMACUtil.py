#!/usr/bin/python
# -*- coding: utf-8 -*-

import http.client
import urllib
import json
import hmac
import hashlib
import time
from datetime import datetime

def buildMySign(params,secretKey,url):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) +'&'
    if sign[-1:] == '&' : sign = sign[:-1]

    data = getnonce()+'https://'+url+sign
    return hmac.new(bytes(secretKey.encode("utf8")),data.encode("utf8"),hashlib.sha256).hexdigest()

def getnonce():
    nonce = str('%1.2f' % time.time() ).replace('.','')[-9:]
    return(nonce)

def httpGet(url,resource,params,apikey,sign):
    headers = {
            "Content-type" : "application/x-www-form-urlencoded",
    }
    conn = http.client.HTTPSConnection(url+resource, timeout=10)
    temp_params = ''
    for key in sorted(params.keys()):
        temp_params += key + '=' + str(params[key]) +'&'
    if temp_params[-1:] == '&' : temp_params = temp_params[:-1]
    conn = http.client.HTTPSConnection(url, timeout=10)
    conn.request("GET", resource, temp_params, headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    return json.loads(data)

def httpPost(url,resource,params,apikey,sign,*args,**kwargs):
     headers = {
            "Content-type" : "application/x-www-form-urlencoded",
            "ACCESS-KEY"   : apikey,
            "ACCESS-SIGNATURE"  : sign,
            "ACCESS-NONCE": getnonce()
     }
     conn = http.client.HTTPSConnection(url, timeout=10)
     temp_params = ''
     for key in sorted(params.keys()):
         temp_params += key + '=' + str(params[key]) +'&'
     if temp_params[-1:] == '&' : temp_params = temp_params[:-1]
     conn.request("POST", resource, temp_params, headers)
     response = conn.getresponse()
     data = response.read().decode('utf-8')
     params.clear()
     conn.close()
     if kwargs["list_mode"]:
         return data
     return json.loads(data)
