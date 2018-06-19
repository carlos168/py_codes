#!/usr/bin/env python
# coding: utf-8

import os
import datetime
import time
import pyjsonrpc
import re

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def getBlock(block_hash):
    #print block_hash
    http_client = pyjsonrpc.HttpClient(
        url = "http://10.81.232.151:9332",
        username = "BW_WALLET_LTC",
        password = "THIS_IS_BW_PASSWORD"

        #url = "http://192.168.2.201:19332",
        #username = "BW_WALLET_LTC",
        #password = "THIS_IS_BW_PASSWORD"
        )

    blockinfo = http_client.call("getblock", block_hash)
    #print blockinfo
    return blockinfo

def getCkpoolLog(logfile):
    fread = open(logfile, "r")
    lines = fread.readlines()
    print "    接收块时间           报块时间          延时(秒)  块高    块hash"
    for line in lines:
        #print line
        if line.find("New block found HASH")>0:
            recv_time = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})", line).group(0)
            recv_hash = line[line.rfind(": ")+2:]
            #print "recv_time: %s, recv_hash: %s" % (recv_time, recv_hash)
            
            ltc_block = getBlock(recv_hash)
            block_timestamp = ltc_block["time"]
            block_hash = ltc_block["hash"]
            block_height = ltc_block["height"]

            recv_timestamp = int(time.mktime(time.strptime(recv_time, "%Y-%m-%d %H:%M:%S")))
            time_delay = recv_timestamp - block_timestamp

            print "%s    %s    %s    %s    %s" % (recv_time, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(block_timestamp)), time_delay, block_height, block_hash)
            time.sleep(2)
        else:
            print "dddddddddd"
    fread.close()

'''
fo = open("ips.txt", "a")
fo.write("%s\n" % ip)
fo.close()
'''
#print http_client.call("/")


if __name__ == "__main__":
    getCkpoolLog("./ltc_ckpool_block.log")
