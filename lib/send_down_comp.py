#!/usr/bin/env python
#coding=utf-8
import urllib2
from auth import mylogger
from  config import *
from send_mail import SendMail
import hashlib
import time
import socket
#import ansible.runner

#机房下线发送机房信息给接口
def SendInfo(url,data):
    url = url + '?' + "key=" + data['key'] + '&' + "compRoom=" + data['compRoom'] + '&' + "flag=" +  data['flag'] + "&" + "nowtime=" + data['nowtime']
    mylogger.info("The room down requested URL is:%s" % url)
    try:
        req = urllib2.Request(url.encode("utf8"))
        response = urllib2.urlopen(req)
    except Exception as e:
        mylogger.info('The server could not fulfill the request,%s' % e)
    else:
        mylogger.info("The room down received response is:%s" % response.read().strip())
        return True

#获取参数的md5值
def Md5Key(KeySrc):
    m2 = hashlib.md5()
    m2.update(KeySrc.encode("utf8"))
    return m2.hexdigest()

#测试端口的连同性    
def CheckNet(SwitchIP):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(10)
    res = True
    try:
        sk.connect((SwitchIP,23))
        mylogger.info('remote addr  %s conn success' % SwitchIP)
    except Exception:
        mylogger.info('remote addr %s conn false' % SwitchIP)
        res = False
    sk.close()
    return res
    
#检测存储连同性，暂时没有用
def CheckStore(url):
    res = True
    try:
        response = urllib2.urlopen(url)
    except Exception as e:
        print 'The server could not fulfill the request.'
        print 'Error code: ', e
        res = False
    else:
        if response != "ok":
           res = False 
    return res


#检测服务器连同性，暂时没有用
def CheckServer(cmd,RoomName):
    res = True
    runner = ansible.runner.Runner(
    module_name = 'shell',
    module_args = cmd,
    pattern = RoomName,
    forks=10)
    results = runner.run()
    num = 0
    for (hostname,result) in results['contacted'].items():
    #print hostname,result['stdout']
        if result['stdout'] == "1":
            num = num + 1
    print num
    if num == 0:
        res = False
    return res
        
              
#触发下线接口 
def do(compRoom,flag):
    Data = {}
    Data['compRoom'] = compRoom
    Data['flag'] = str(flag)
    Data['nowtime'] = str(int(time.time()))
    KEY = HASHKEY + Data['nowtime'] + Data['flag']
    Data['key'] = Md5Key(KEY) 
    SendInfo(RoomUrl,Data)

#流量异常时检测5次，如果都正常发送警告邮件，不通时触发下线接口
def NetDown(SwitchIP,compRoom):
    num = 0
    flag = 0
    for i in range(5):
        NetStatus = CheckNet(SwitchIP)
        if not NetStatus:
            num = num + 1
        time.sleep(2)
    if num == 5:
        mylogger.info("###########5 connect fail,going to down #############")
        do(compRoom,flag)
        return True
    else:
        mylogger.info("###########5 connect success,going to mail #############")
        SendMail(compRoom)
         
         
         
if __name__ == '__main__':
    NetDown(SwitchIP,compRoom)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
