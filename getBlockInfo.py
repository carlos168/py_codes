#!/usr/bin/env python
#encoding=utf-8

import urllib
import urllib2
import ssl 

import json
import time
import sys 
reload(sys)
sys.setdefaultencoding('utf8')

'''
char *tmp;
    char hoststr[32] = {0};
    char queryCmd[512];
    char coinbaseStr[256];
    int querylen, postlen;

    httpPost = StringSize(1000);

    snprintf(queryCmd, 512,
             "{\"jsonrpc\":\"1.0\",\"id\":\"20180117\",\"method\":\"getblock\",\"params\":[\"%s\"]}",
             strhash);
    querylen = (int) strlen(queryCmd);
    sprintf(hoststr, "%s:%d", ipv4str, eth_portnum);
    //写成http消息
    tmp = httpPost;
    tmp += sprintf(tmp, "POST / HTTP/1.1\r\nHOST: %s\r\nAuthorization: Basic QldfV0FMTEVUX0xUQzpUSElTX0lTX0JXX1BBU1NXT1JE\r\nContent-Type: application/json\r\nContent-length: %d\r\n\r\n%s\r\n",
                   hoststr,
                   querylen,
                   queryCmd);

    postlen = (int) (tmp - httpPost);

'''



def getBlockInfo():
    print 'getBlockInfo()'
    
    url = 'http://192.168.2.201:8332'
    data = {
        "jsonrpc": "1.0",
        "id": "20180117",
        "method": "getblock",
        "params": ["00000000000000000000b482afd6102b9a9e691dd1caecad57bea05e952239d3"]
    }

    headers = {
        "Authorization": "Basic QldfV0FMTEVUX0xUQzpUSElTX0lTX0JXX1BBU1NXT1JE"
    }

    req = urllib2.Request(url, data=json.dumps(data,ensure_ascii=False).encode('utf-8'), headers=headers)
    try:
        response = urllib2.urlopen(req)
        print "HTTP return code:%d" % response.getcode()
        if 200 == response.getcode():
            strResult= response.read()
            print strResult
            # result_json = json.loads(strResult)
    except Exception ,ex:
        print "Found Error :%s" % str(ex)
         # print response.text

def test():
    import urllib
    import httplib 
    test_data = {
        "jsonrpc": "1.0",
        "id": "20180117",
        "method": "getblock",
        "params": ["00000000000000000000b482afd6102b9a9e691dd1caecad57bea05e952239d3"]
    }
    test_data_urlencode = urllib.urlencode(test_data)
    requrl = "http://192.168.2.201:8332"
    headerdata = {
        "Authorization": "Basic QldfV0FMTEVUX0xUQzpUSElTX0lTX0JXX1BBU1NXT1JE"
    }
    conn = httplib.HTTPConnection("192.168.2.201:8332")
    conn.request(method="POST",url=requrl,body=test_data_urlencode,headers = headerdata) 
    response = conn.getresponse()
    res= response.read()
    print res

#def test2():
    #from jsonrpc import ServiceProxy
  
    #access = ServiceProxy("http://user:password@192.168.2.201:8332")
    #access.getinfo()
    #access.listreceivedbyaddress(6)
    
    #access.sendtoaddress("11yEmxiMso2RsFVfBcCa616npBvGgxiBX", 10)


if __name__ == '__main__':
    print 'test'
    #test()
    getBlockInfo()

