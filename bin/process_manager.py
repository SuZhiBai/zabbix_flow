#!/usr/bin/env python
#coding=utf-8
import os, sys, time
BasePath = '/'.join(sys.path[0].split('/')[:-1])
LibPath = BasePath + "/lib"
sys.path.append(LibPath)
from get_data import *
if __name__ == '__main__':
    mylogger.info("*" * 100)
    done()
