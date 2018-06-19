#!/usr/bin/env python   
#encoding=utf-8

import base64   
import urllib   
import httplib   
   
#params是你传递的参数，我的场景里是json字符串。   
data = { 
    "jsonrpc": "1.0",
    "id": "20180117",
    "method": "getblock",
    "params": ["00000000000000000000b482afd6102b9a9e691dd1caecad57bea05e952239d3"]
}
params = urllib.urlencode(data)   
#auth就是登录认证的key，要通过base64编码，所以上面要import进来   
auth = base64.b64encode('BW_WALLET_BTC'+ ':'+ 'THIS_IS_BW_PASSWORD')  
#将认证和请求格式信息放入请求头中，这里注意，后面要加入json请求格式的说明，否则会报http 415格式错误   
#headers = {"Authorization": "Basic QldfV0FMTEVUX0xUQzpUSElTX0lTX0JXX1BBU1NXT1JE", "Content-Type": "application/json"}
headers = {"Authorization": "Basic "+auth, "Content-Type": "application/json"}
try:
    #建立连接   
    conn = httplib.HTTPConnection("192.168.2.201:8332")
    #发送请求   
    conn.request("POST","/", str(params), headers)
    response = conn.getresponse()
    print 'dddddddd'
    print response
    print response.status  
    print response.read()
except Exception, ex:
    print "Found Error: %s" % str(ex)


