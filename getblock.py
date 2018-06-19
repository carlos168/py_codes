#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc

http_client = pyjsonrpc.HttpClient(
    #url = "http://182.92.172.75:8332",
    #username = "BW_WALLET_BTC",
    #password = "THIS_IS_BW_PASSWORD"

    url = "http://192.168.2.201:8332",
    username = "STAFF",
    password = "STAFF_PASSWORD"
)
print http_client.call("getblock", "0000000000000000001be4b60c43a17072d7e51d3bd40c5f5b40a2b8412e0e1a")
#print http_client.call("/")
