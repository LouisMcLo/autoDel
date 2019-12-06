# encoding: utf-8

##############################################################################
#   Function: Schedule Clean Expire File                                     #
#   Author:                                              #
#   Date:                                                     #
##############################################################################
'''
import sys, os
import argparse

parser = argparse.ArgumentParser(description='clean expire file script')
parser.add_argument('--stdin',  type=str, default = '/dev/null')
parser.add_argument('--stdout', type=str, default = '/dev/null')
parser.add_argument('--stderr', type=str, default = '/dev/null')
parser.add_argument('--cpath',  type=str, default = '')
args = parser.parse_args()
'''
from file.clean.task import ScanTask
from file.clean import get_conf

if __name__ == '__main__':
    #cpath = args.cpath
    #cpath=[]
    for i in range(1,6):
        cpath=get_conf('clean_path{}'.format(i), None)
        if cpath != '':
            scanTask = ScanTask("clean-thread-{}".format(i), cpath)
            scanTask.start()
