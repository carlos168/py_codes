#!/usr/bin/env python
#encoding=utf-8

import simplejson
import httplib2
import httplib
from datetime import datetime


def checkUrlAlive(url):
    try:
        if url.find("http://") != -1:
            newUrl = url.replace("http://","")
        elif url.find("https://") != -1:
            newUrl = url.replace("https://","")
        else:
            newUrl = url
        print newUrl
        return newUrl
    except Exception as e:
        print "website_get_newUrl():"+str(e)


def website_urlopen_reuslt(url):
    '''
    @访问url,获取返回结果
    @return 元组
    '''
    print ("===1 == website_urlopen_reuslt =====")
    try:
        domain,host,urlsuffix,port = ("www.baidu.com", "www.baidu.com", "/", "80")
        header = {"Host":host}
        h=httplib2.Http('.cache',timeout=2)
        try:
            response,content = h.request(url)
            print ("===2 == website_urlopen_reuslt ===== response,content ======")
        except httplib.BadStatusLine as e:
            result = {"responsetime":0,"status":str(e)}
            print ("===3 == website_urlopen_reuslt ===== str(0),simplejson.dumps(result),str(1),str(e) = %s, %s, %s, %s ======" % (str(0),simplejson.dumps(result),str(1),str(e)))
            return str(0),simplejson.dumps(result),str(1),str(e)
        except Exception as e:
            result = {"responsetime":0,"status":str(e)}
            print("==4 === website_urlopen_reuslt ===== str(0),simplejson.dumps(result),str(1),str(e) = %s, %s, %s, %s ======" % (str(0),simplejson.dumps(result),str(1),str(e)))
            return str(0),simplejson.dumps(result),str(1),str(e)
            
            
        start = datetime.now()
        status = response['status']
        end = datetime.now()
    except Exception as e:
        print("website_urlopen_result():"+str(e))
        result = {"responsetime":0,"status":str(e)}
        print("===5 == website_urlopen_reuslt = %s, %s, %s, %s ====" % (str(0),simplejson.dumps(result),str(1),str(e)))
        return str(0),simplejson.dumps(result),str(1),str(e)
        
    responsetime = (end - start).microseconds / 1000
    result = {"responsetime":responsetime,"status":str(status)}
    print("===6 == website_urlopen_reuslt ===== str(1),simplejson.dumps(result),content,status = %s, %s, %s, %s=====" % (str(1), simplejson.dumps(result),content, status))
    return str(1),simplejson.dumps(result),content,status


if __name__ == "__main__":
    # checkUrlAlive("https://www.baidu.com")

    website_urlopen_reuslt("https://www.baidu.com")

