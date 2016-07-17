#!/usr/bin/python
# -*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from auth import mylogger
from  config import *


def SendMail(comproom):
    message = MIMEText("%s network exception,please note!" % comproom, 'plain', 'utf-8')
    subject = "%s network exception" % comproom
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        mylogger.info("send mail success")
    except smtplib.SMTPException:
        mylogger.info("send mail fail")

if __name__ == '__main__':
    SendMail(comproom)