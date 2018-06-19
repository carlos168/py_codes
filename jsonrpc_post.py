#!/usr/bin/env python
#encoding=utf-8
 
import json,urllib2

textmod = {
    "jsonrpc": "1.0",
    "id":"20180117",
    "method":"getblock",
    "params":["000000000000000000047c7d1f64d46109668064b0bcb573e075640597919a5e"]
}
textmod = json.dumps(textmod)
print(textmod)

header_dict = {
    'Authorization': 'Basic QldfV0FMTEVUX0xUQzpUSElTX0lTX0JXX1BBU1NXT1JE',
    "Content-Type": "application/json",
    "Content-length": len(textmod)
}
print header_dict

url='http://192.168.2.201:8332/'
try:
    req = urllib2.Request(url=url,data=textmod,headers=header_dict)
    res = urllib2.urlopen(req)
    res = res.read()
    print(res)
except Exception, ex:
    print "error: %s" % str(ex)

