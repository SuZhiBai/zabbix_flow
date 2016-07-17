
#!/usr/bin/env python
#coding=utf-8
import json
import urllib2
from get_items import *
import hashlib
import urllib
from send_down_comp import *

#获取流量信息,包括交换机，流量和时间戳信息，如[{u'itemid': u'62995', u'ns': u'217370136', u'value': u'887950384', u'clock': u'1464661375'}]
def GetData(AuthID,limit,ItemId):
    data = json.dumps(
    {
       "jsonrpc":"2.0",
       "method":"history.get",
       "params":{
           "output":"extend",
           "history":'3',
           "sortfield":'clock',
           "sortorder":'DESC',
           "itemids":ItemId,
           "limit":limit
       },
       "auth":AuthID,
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
        mylogger.info("Data taken from zabbix is:%s" % response['result'])
        if response['result'] == []:
            return "nook"
        for host in response['result']:
            return host

#发送流量给高庆山写好的接口
def SendInfo(url,data):
    url = url + '?' + "key=" + data['key'] + '&' + "compRoom=" + data['cnmpRoom'] + '&' + "flow=" +  data['flow'] + "&" + "nowtime=" + data['nowtime']
    mylogger.info("The requested URL is:%s" % url)
    try:
        req = urllib2.Request(url.encode("utf8"))
        response = urllib2.urlopen(req)
    except Exception as e:
        mylogger.info('The server could not fulfill the request:%s'% e)
    else:
        mylogger.info("The received response is:%s" % response.read().strip())
        return True

#获取接口参数的md5值
def Md5Key(KeySrc):
    m2 = hashlib.md5() 
    m2.update(KeySrc.encode("utf8"))
    return m2.hexdigest()

def done():
    Data = {}
    GroupId = GetGroup(AuthId,url,GroupName)
    HostIdList = GetHost(AuthId,url,GroupId)
    for HostInfo in HostIdList:
        Data['cnmpRoom'] = HostInfo['name'].split('-')[0]
        SwitchIP = HostInfo['name'].split('-')[1]
        if HostInfo['name'].encode('utf8') in ItemNameDict:
            ItemInfo = GetItem(AuthId,url,HostInfo)
            IitemsHost = GetData(AuthId,limit,ItemInfo[0]['itemid'])
            Data['flow'] = str(int(IitemsHost['value'])/1024/1024)
            Data['nowtime'] = IitemsHost['clock']
            IntervalTime = int(time.time()) - int(Data['nowtime'])
            #流量异常时，触发检测
            if IntervalTime >60 or Data['flow'] == str(0) or IitemsHost == 'nook':
                mylogger.info("########## %s network exception,into check script #######" % Data['cnmpRoom'])
                NetDown(SwitchIP,Data['cnmpRoom'])
                continue
            #KeySrc = HASHKEY + Data['nowtime'] + Data['cnmpRoom'] + Data['flow']
            KeySrc = HASHKEY + Data['nowtime']  + Data['flow']
            Data['key'] = Md5Key(KeySrc)
            mylogger.info("Send data for:%s" % Data)
            SendInfo(FlowUrl,Data)
        else:
            mylogger.info("##########%s is not items! ###########################" % Data['cnmpRoom'])
            continue
if __name__ == "__main__":
    done()
