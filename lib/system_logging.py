#!/usr/bin/env python
#coding=utf-8
import os
import sys
import time
import logging
import logging.handlers
BasePath = '/'.join(sys.path[0].split('/')[:-1])
ConfigPath = BasePath + "/config"
sys.path.append(ConfigPath)
from  config import *
#filename=file_name  log out to terminal
def tofile(file_name):
        myformat = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
        #logging.basicConfig(level=logging.DEBUG,format=myformat,filename=file_name,filemode='a')
        logging.basicConfig(level=logging.DEBUG,format=myformat)
        file_path = os.path.join(LOGGER_DIR, file_name)
        Rthandler = logging.handlers.TimedRotatingFileHandler(file_path, 'H', 12, 60)
        Rthandler.setLevel(logging.INFO)
        formatter = logging.Formatter(myformat)
        Rthandler.setFormatter(formatter)
        Rthandler.suffix = "%Y%m%d-%H%M.log"
        logging.getLogger('').addHandler(Rthandler)
        return logging
