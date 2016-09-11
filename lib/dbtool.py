#!/usr/bin/env python
#encoding:utf8
import json
import time,random
import datetime
import MySQLdb
import MySQLdb.cursors

class DB: 
    conn = None
    db = None
    host = None

    def __init__(self, host, mysql_user, mysql_pass, mysql_db):
        self.host = host
        self.mysql_user = mysql_user
        self.mysql_pass = mysql_pass
        self.mysql_db = mysql_db
    def connect(self):
        self.conn = MySQLdb.connect(host=self.host, user=self.mysql_user, passwd=self.mysql_pass, db=self.mysql_db, charset="utf8", connect_timeout=600, compress=True,cursorclass = MySQLdb.cursors.DictCursor)
        self.conn.autocommit(True)
    def execute(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except (AttributeError, MySQLdb.OperationalError):
            try:
                cursor.close()
                self.conn.close()
            except:
                pass
            time.sleep(1)
            try:
                self.connect()
                print "reconnect DB"
                cursor = self.conn.cursor()
                cursor.execute(sql)
            except (AttributeError, MySQLdb.OperationalError):
                time.sleep(2)
                self.connect()
                print "reconnect DB"
                cursor = self.conn.cursor()
                cursor.execute(sql)
    
        return cursor
