#!/usr/bin/env python2.7
#coding=utf-8
import json
import urllib2
from auth import *
GroupName = 'switchs'

AuthId = ZabbixAuth(url,user,password)

#传入zabbix中定义的组名GroupName，获取GroupId
def GetGroup(AuthId,url,GroupName):
    data = json.dumps(
    {
       "jsonrpc":"2.0",
       "method":"hostgroup.get",
       "params":{
           "output":["groupid","name"],
       },
       "auth":"%s" % AuthId, 
       "id":1,
    })
    request = urllib2.Request(url,data)
    for key in header:
        request.add_header(key,header[key])
    try:
        result = urllib2.urlopen(request)
    except Exception as e:
        mylogger.info("The server could not fulfill the request:%s" % e)
    else:
        response = json.loads(result.read())
        result.close()
        for group in response['result']:
            if group['name'] == GroupName:
                mylogger.info("Group Id:%s\tGroupName:%s" % (group['groupid'],group['name']))
                GroupId = group['groupid']
        return GroupId

#传入GroupId,获取这个组中所有监控交换机的HostId,HostName,日志中有对应输出
# 类似 HostID:10428	HostName:中山电信-
def GetHost(AuthId,url,GroupId):      
    data = json.dumps(
    {
        "jsonrpc":"2.0",
        "method":"host.get",
        "params":{
            "output":["hostid","name"],
            "groupids":GroupId,
        },
        "auth":AuthId,
        "id":1,
    })

    request = urllib2.Request(url,data)
    for key in header:
        request.add_header(key,header[key])

    try:
        result = urllib2.urlopen(request)
    except Exception as e:
        mylogger.info('The server could not fulfill the request:%s'% e)
    else:
        response = json.loads(result.read())
        result.close()
        mylogger.info("Number Of Hosts:%s" % len(response['result']))
        for host in response['result']:
            mylogger.info("HostID:%s\tHostName:%s" % (host['hostid'],host['name']))
        return response['result']

#传入每个监控主机的HostId，获取监控项item信息，包括ItemId和ItemName(即端口信息) 如： ItemID:62995	ItemName:ifHCOutOctets[GigabitEthernet0/2]     
def GetItem(AuthId,url,HostInfo):
    data = json.dumps(
    {
       "jsonrpc":"2.0",
       "method":"item.get",
       "params":{
           "output":["itemids","key_"],
           "hostids":"%s" % HostInfo['hostid'],
           "search":{"key_":ItemNameDict[HostInfo['name'].encode('utf8')]}
       },
       "auth":"%s" % AuthId,
       "id":1,
    })

    request = urllib2.Request(url,data)
    for key in header:
        request.add_header(key,header[key])
    try:
        result = urllib2.urlopen(request)
    except Exception as e:
        mylogger.info('The server could not fulfill the request:%s'% e)
    else:
        response = json.loads(result.read())
        result.close()
        #mylogger.info("Number Of Hosts:%s" % len(response['result']))
        ress = response['result']
        mylogger.info("HostName:%s"%HostInfo['name'])
        for res in ress:
            mylogger.info("ItemID:%s\tItemName:%s" % (res['itemid'],res['key_']))
        return ress

if __name__ == "__main__":
    GroupId = GetGroup(AuthId,url,GroupName)
    HostIdList = GetHost(AuthId,url,GroupId)
    for HostInfo in HostIdList:        
        mylogger.info(GetItem(AuthId,url,HostInfo))

