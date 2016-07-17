#!/usr/bin/env python
#coding=utf-8
#
import json
import urllib2
import sys
import system_logging
from config import *
mylogger = system_logging.tofile('console.log')
header = {"Content-Type":"application/json"}
#传入zabbix的用户名和密码，取得zabbix api的认证ID，以后连接，都需要传入此ID做为认证
def ZabbixAuth(url,user,password):
    data = json.dumps(
    {
       "jsonrpc": "2.0",
       "method": "user.login",
       "params": {
       "user": "%s" % user,
       "password": "%s" %  password
    },
    "id": 0
    })

    request = urllib2.Request(url,data)
    for key in header:
       request.add_header(key,header[key])

    try:
       result = urllib2.urlopen(request)
    except Exception as e:
       mylogger.info("Auth Failed, Please Check Your Name AndPassword:%s" % e)
    else:
       response = json.loads(result.read())
       result.close()
       mylogger.info("Auth Successful. The Auth ID Is:%s" % (response['result']))
       return response['result']
if __name__ == '__main__':
    ZabbixAuth(url,user,password)
       
