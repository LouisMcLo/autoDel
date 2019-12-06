# encoding: utf-8

##############################################################################
#   Function: 配置与日志                            #
#   Author:                                             #
#   Date:                                                      #
##############################################################################


__all__ = ['fileutils','task']

import os
import configparser
from logging.handlers import TimedRotatingFileHandler
import logging
import sys
###########################################################################################################################
#__file__为本文件地址
#os.path.dirname（）文件的上层文件夹地址,但是打包成exe之后失效
#conf_path = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","config.ini"))
#os.path.abspath(sys.argv[0]))执行文件的路径
conf_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])),"config.ini")
#print(conf_path)
sys_conf = configparser.ConfigParser()
#.ini中有中文需要加encoding=“utf-8-sig”否则报错
sys_conf.read(conf_path,encoding='UTF-8-sig')

###########################################################################################################################

log_folder = os.path.abspath(os.path.dirname(sys_conf.get('sys', 'log_file')))
if not os.path.exists(log_folder):
    os.makedirs(log_folder)
handler = TimedRotatingFileHandler(sys_conf.get('sys', 'log_file'), backupCount=7, interval=1, when="D")
handler.setFormatter(logging.Formatter('[%(process)d][%(asctime)s][%(threadName)s][%(levelname)s]-| %(message)s'))
logger = logging.getLogger('')
logger.setLevel(logging.INFO)
logging.getLogger('').addHandler(handler)
console = logging.StreamHandler()
console.setFormatter(logging.Formatter('[%(process)d][%(asctime)s][%(threadName)s][%(filename)s][line:%(lineno)d] %(levelname)s-| %(message)s'))
console.setLevel(logging.DEBUG)
logging.getLogger('').addHandler(console)

###########################################################################################################################
def get_conf(key, default):
    if sys_conf.has_option("sys", key):
        return sys_conf.get("sys", key)
    else:
        return default

class CleanError(Exception):
    def __init__(self, message):
        self.__message = message
    def __str__(self):
        return repr(self.__message)
