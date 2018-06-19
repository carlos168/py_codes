#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json

test = {"ID": "2", "IP":"12.12.12.12", "Port": "3000", "测试": "测试内容"}
print type(test)
#data= json.loads(test)
#print data
#输出结果:"2"
data = json.dumps(test)
print data
print type(data)

data2 = json.loads(data)
print data2
print type(data2)
#输出结果:{"ID": "2", "IP":"12.12.12.12", "Port": "3000"}

