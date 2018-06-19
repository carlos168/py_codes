#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import ssl 

import json
import time
# import datetime
# import requests
import sys 
# import getopt
# from requests.exceptions import RequestException
reload(sys)
sys.setdefaultencoding('utf8')

def https_test():
    print 'ddddd'

#查询所有用户的openid列表
def getOpenidList(access_token, next_openid):
    openids = []

    while True:
        wxurl = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s' % (access_token, next_openid)
        req = urllib2.Request(wxurl)
        try:
            response = urllib2.urlopen(req)
            print "HTTP return code:%d" % response.getcode()
            if (200 == response.getcode()):
                strResult= response.read()
                result_json = json.loads(strResult)
                total = result_json["total"]
                count = result_json["count"]
                next_openid = result_json["next_openid"]
                if (count>0 and len(result_json["data"]["openid"])>0):
                    openids += result_json["data"]["openid"]
                if (total == count) or (count == 0):
                    break
            else:
                break
        except Exception ,ex:
            print "Found Error :%s" % str(ex)
    return openids
    

#批量查询用户基本信息
def getUserInfoList(access_token, openid_list):
    user_info_list = []

    wxurl = 'https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token=%s' %access_token

    user_list = []
    for openid in openid_list:
        user_list.append({"openid": openid, "lang": "zh_CN"})
        if len(user_list)==100:
            data = {'user_list': user_list}
            req = urllib2.Request(wxurl, data=json.dumps(data,ensure_ascii=False).encode('utf-8'))
            try:
                response = urllib2.urlopen(req)
                print "HTTP return code:%d" % response.getcode()
                if 200 == response.getcode():
                    strResult= response.read()
                    #print strResult

                    result_json = json.loads(strResult)
                    #print result_json
                    user_infos = result_json["user_info_list"]
                    for user_info in user_infos:
                        user_info_list.append({"openid": user_info["openid"], "nickname": user_info["nickname"]})
                        #print user_info["openid"], user_info["nickname"]
                    user_infos = []
            except Exception ,ex:
                print "Found Error :%s" % str(ex)
            user_list = []

    if len(user_list)>0:
        data = {'user_list': user_list}
        req = urllib2.Request(wxurl, data=json.dumps(data,ensure_ascii=False).encode('utf-8'))
        try:
            response = urllib2.urlopen(req)
            print "HTTP return code:%d" % response.getcode()
            if 200 == response.getcode():
                strResult= response.read()
                #print strResult

                result_json = json.loads(strResult)
                #print result_json
                user_infos = result_json["user_info_list"]
                for user_info in user_infos:
                    user_info_list.append({"openid": user_info["openid"], "nickname": user_info["nickname"]})
                    #print user_info["openid"], user_info["nickname"]
                user_infos = []

        except Exception ,ex:
            print "Found Error :%s" % str(ex)
    return user_info_list


#查询用户基本信息
def getUserInfoByOpenid(access_token, openid):
    nickname = ''

    wxurl = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN" % (access_token, openid)
    req = urllib2.Request(wxurl)

    try:
        response = urllib2.urlopen(req)
        print "HTTP return code:%d" % response.getcode()
        if 200 == response.getcode():
            strResult= response.read()
            print strResult
            
            result_json = json.loads(strResult)
            nickname = result_json["nickname"]

    except Exception ,ex:
        print "Found Error :%s" % str(ex)
    return nickname

def getTags(access_token):
    wxurl = 'https://api.weixin.qq.com/cgi-bin/tags/get?access_token=%s' % access_token
    req = urllib2.Request(wxurl)

    try:
        response = urllib2.urlopen(req)
        print "HTTP return code:%d" % response.getcode()
        if 200 == response.getcode():
            strResult= response.read()
            print strResult
            result_json = json.loads(strResult)

    except Exception ,ex:
        print "Found Error :%s" % str(ex)


def getTagByName(access_token, tag_name):
    tag_info = {}

    wxurl = 'https://api.weixin.qq.com/cgi-bin/tags/get?access_token=%s' % access_token
    req = urllib2.Request(wxurl)

    try:
        response = urllib2.urlopen(req)
        print "HTTP return code:%d" % response.getcode()
        if 200 == response.getcode():
            strResult= response.read()
            # print strResult
            result_json = json.loads(strResult)
            for item in result_json["tags"]:
                if item["name"] == tag_name:
                    tag_info = item
                    break

    except Exception ,ex:
        print "Found Error :%s" % str(ex)
    return tag_info


def getTagOpenidList(access_token, tagid):
    openid_list = []

    wxurl = 'https://api.weixin.qq.com/cgi-bin/user/tag/get?access_token=%s' % access_token
    data = {"tagid": tagid, "next_openid": ''}
    req = urllib2.Request(wxurl, data=json.dumps(data,ensure_ascii=False).encode('utf-8'))
    try:
        response = urllib2.urlopen(req)
        print "HTTP return code:%d" % response.getcode()
        if 200 == response.getcode():
            strResult= response.read()
            result_json = json.loads(strResult)
            count = result_json["count"]
            if count>0 and len(result_json["data"]):
                openid_list += result_json["data"]["openid"]

    except Exception ,ex:
        print "Found Error :%s" % str(ex)

    return openid_list


def getTagUserInfoList(access_token, tagid):
    openid_list = []

    wxurl = 'https://api.weixin.qq.com/cgi-bin/user/tag/get?access_token=%s' % access_token
    data = {"tagid": tagid, "next_openid": ''}
    req = urllib2.Request(wxurl, data=json.dumps(data,ensure_ascii=False).encode('utf-8'))
    try:
        response = urllib2.urlopen(req)
        print "HTTP return code:%d" % response.getcode()
        if 200 == response.getcode():
            strResult= response.read()
            result_json = json.loads(strResult)
            count = result_json["count"]
            if count>0 and len(result_json["data"]):
                openid_list += result_json["data"]["openid"]

    except Exception ,ex:
        print "Found Error :%s" % str(ex)

    return openid_list


def sendTempMsgAlarm(access_token, tempid, openid_list, msg):
    wxurl = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % access_token

    data = {
        "template_id": tempid,  #"CDxglUcjTlGjzC2qsOYru7_qI0rxAlSM5GcxtQ9n6lM",
        "data": {
            "first": {
                "value": "%s服务器[%s]异常告警" % ("hostname", "serverip"),
                "color": "#173177"
            },
            "keyword1": {
                "value": "hostname", #"告警系统名称",
                "color": "#173177"
            },
            "keyword2": {
                "value": "localtime", #"告警时间",
                "color": "#173177"
            },
            "keyword3": {
                "value": "LOGEMERG", #"告警级别",
                "color": "#173177"
            },
            "remark": {
                "value": msg,
                "color": "#173177"
            }
        }
    }
    for openid in openid_list:
        data["touser"] = openid
            # response = requests.post(wxurl, data = json.dumps(data,ensure_ascii=False).encode('utf-8'))
        req = urllib2.Request(wxurl, data=json.dumps(data,ensure_ascii=False).encode('utf-8'))
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
        # except RequestException as e :
        #     print "get_users failed, the response is :%s" % response.text
        data["touser"] = ""


def sendMsg(access_token, openid):
    # https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=
    # wxurl = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % access_token
    wxurl = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=9_JpeKvQiD8FGVqV9wbVZl1NHVlT6NAYa19Ar-7e8YbUOwEXLDyN49nCR4yAb7BA_MOJGadKcUs7vN_28alF7yMdYvZqRaBS6-FZJbPI7J7Zp7BYWTUBnbqQFwZL20g4-ZRRNkENNZgiueUeQSHPXcAEAPXF'
    data = { 
        "template_id": "CDxglUcjTlGjzC2qsOYru7_qI0rxAlSM5GcxtQ9n6lM",
        "data": {
            "first": {
                "value": "%s服务器[%s]异常告警" % ("hostname", "serverip"),
                "color": "#173177"
            },  
            "keyword1": {
                "value": "hostname", #"告警系统名称",
                "color": "#173177"
            },  
            "keyword2": {
                "value": time.strftime('%Y-%m-%d %H:%M:%S'), #"告警时间",
                "color": "#173177"
            },
            "keyword3": {
                "value": "LOGEMERG", #"告警级别",
                "color": "#173177"
            },  
            "remark": {
                "value": "alarm_content",
                "color": "#173177"
            }   
        }   
    }
    data["touser"] = openid
            # response = requests.post(wxurl, data = json.dumps(data,ensure_ascii=False).encode('utf-8'))
    req = urllib2.Request(wxurl, data=json.dumps(data,ensure_ascii=False).encode('utf-8'))
    try:
        response = urllib2.urlopen(req)
        print "HTTP return code:%d" % response.getcode()
        if 200 == response.getcode():
            strResult= response.read()
            print strResult
            # result_json = json.loads(strResult)

    except Exception ,ex:
        print "Found Error :%s" % str(ex)


def saveFile(filename, user_info_list):
    with open(filename, 'w+') as f:
        for item in user_info_list:
            f.write("%s %s\n" % (item["openid"], item["nickname"]))

if __name__ == '__main__':
    access_token = '9_YgSOEREstTm5Oxal0tHpnkGxOsHeEgPSRndlprpksGZy1S57SRjTLtLxJOq0JvCFMQT55QCYu_PtNyV2nJJ2MD-QMa5JuPqdMDui6TFL7kByBgogPURCH_1oyRSJQHj_SFEPzF0n8Bta0oNPWXHcAGAJKU'

    # openid_list = getOpenidList(access_token, '')
#    print openid_list
    # print len(openid_list)

    # user_info_list = getUserInfoList(access_token, openid_list)
    # print len(user_info_list)
    # saveFile("openid_nickname.txt", user_info_list)

    # nickname = getUserInfoByOpenid(access_token, 'oNoka0yGzTIjRIWuShgn8u2AJmOs')
    # print nickname

############
    # getTags(access_token)
    # tag_info = getTagByName(access_token, "运营部")
    # print tag_info["id"], tag_info["name"], tag_info["count"]

    # openid_list = getTagOpenidList(access_token, tag_info["id"])
    # print openid_list

    # tagUsersInfo = getUserInfoList(access_token, openid_list)
    # print tagUsersInfo

    # sendTempMsgAlarm(access_token, 'CDxglUcjTlGjzC2qsOYru7_qI0rxAlSM5GcxtQ9n6lM', openid_list, "发送告警测试（备注内容）")
##############
    sendMsg(access_token, "oNoka0yGzTIjRIWuShgn8u2AJmOs")
    




