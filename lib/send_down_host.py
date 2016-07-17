#!/usr/bin/env python
#coding=utf-8
import urllib2
import system_logging
from  config import *
import hashlib
import time
from flask import Flask,request
app = Flask(__name__)

def SendInfo(url,data):
    url = url + '?' + "key=" + data['key'] + '&' + "cabinetIP=" + data['cabinetIP'] + '&' + "flag=" +  data['flag'] + "&" + "nowtime=" + data['nowtime']
    print url
    try:
        req = urllib2.Request(url.encode("utf8"))
        response = urllib2.urlopen(req)
    except Exception as e:
        print 'The server could not fulfill the request.'
        print 'Error code: ', e
    else:
        print response.read().strip()


def Md5Key(KeySrc):
    m2 = hashlib.md5()
    m2.update(KeySrc)
    return m2.hexdigest()
 
def  storedata(FileName,HostName):
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(FileName,'a') as f:
        f.write(nowtime + " " + HostName + "\n")
    return True

@app.route('/')
def do():
    Data = {}
    Data['cabinetIP'] = request.args.get('HostName')
    Data['flag'] = request.args.get('flag')
    if Data['flag'] == '0':
        storedata(FileName,Data['cabinetIP'])
    Data['nowtime'] = str(int(time.time()))
    Data['key'] = Md5Key(HASHKEY + Data['nowtime'] + Data['cabinetIP'] + Data['flag']) 
    SendInfo(HostUrl,Data)
    return True
    
if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0')

