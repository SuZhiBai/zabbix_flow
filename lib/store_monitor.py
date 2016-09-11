#!/usr/bin/env python
#coding=utf-8
import system_logging
from config import db_config,ItemNameDict
from dbtool import DB
import urllib2
from send_mail import SendMail
from send_down_comp import do
from auth import mylogger
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
db = DB(host=db_config['host'], mysql_user=db_config['user'], mysql_pass=db_config['passwd'], \
                mysql_db=db_config['db'])
def GetMobileIp(comp_name):
  sql = "select b.compRoomName,c.cabinetIP ,d.serviceTypeCode \
         from ip_comproom_cabinet  a \
         LEFT JOIN ip_comproom b \
         on a.compRoomID = b.compRoomID \
         LEFT JOIN ip_cabinet c \
         on a.cabinetID = c.cabinetID \
         LEFT JOIN ip_servicetype d \
         on a.serviceTypeID = d.serviceTypeID \
         where b.compRoomName = '%s' and d.serviceTypeCode = 'mobile'" % comp_name
  res = db.execute(sql)
  resone = res.fetchone()
  if resone:
    comp_ip = resone['cabinetIP']
    return comp_ip
def CheckUrl(comp_ip):
  url = "http://%s" % comp_ip
  rcode = {'result':0}
  try:
    response = urllib2.urlopen(url,timeout=10)
    if str(response.code) == "200":
      rcode['result'] = 1
  except:
    print comp_ip + "timeout"
  return rcode
def UrlDown(comp_ip,comp_name):
    num = 0
    flag = 0
    for i in range(2):
        ResStatus = CheckUrl(comp_ip)
        if ResStatus['result'] == 0:
            num = num + 1
        time.sleep(2)
    if num == 2:
        mylogger.info("###########5 connect fail,going to down #############")
        #do(compRoom,flag)
        #SendMail(comp_name)
        print comp_name + "going to down" + comp_ip
        return True
    else:
        print comp_name + "is successful-------------------------"

if __name__ == "__main__":
  for comp_name in ItemNameDict:
    comp_name = comp_name.split('-')[0]
    comp_ip = GetMobileIp(comp_name)
    if comp_ip:
      UrlDown(comp_ip,comp_name) 
