
# encoding: utf-8

##############################################################################
#   Function: 文件集合类                            #
#   Author:                                              #
#   Date:                                                       #
##############################################################################


import os,sys
import os.path,time,datetime
import traceback

def exists(fname):
    return True if os.path.exists(fname) else False

def isdir(fname):
    return True if os.path.isdir(fname) else False

def isfile(fname):
    return True if os.path.isfile(fname) else False

def isimage(fname):
    (_,ext) = os.path.splitext(fname)
    return True if ext=='.jpg' or ext=='.bmp' or ext=='.png' or ext=='.gif' or ext=='.feature' else False

def istype(fname, types):
    (_,ext) = os.path.splitext(fname)
    return True if ext in types else False

def isempty(fname):
    return True if exists(fname) and len(os.listdir(fname))==0 else False

def sctime(fname):
    return os.stat(fname).st_ctime

def smtime(fname):
    return os.stat(fname).st_mtime

def rmdirs(fname):
    try:
        if not exists(fname):
            return 0
        elif not isempty(fname):
            return -1
        else:
            os.removedirs(fname)
            return 1
    except OSError:
        raise Exception("delete dirs {0} exception:{1}".format(fname,traceback.print_exc()))

def rmfile(fname):
    try:
        if not exists(fname):
            return 0
        else:
            os.remove(fname)
            return 1
    except OSError:
        raise Exception("delete file {0} exception:{1}".format(fname,traceback.print_exc()))


def expire(fname, hours=6):
    ntime,ftime = (round(time.time()*1000)),sys.float_info.max
    if hours < 6:
        raise Exception('file expire time less 6 hour')
    elif os.path.isfile(fname):
        ftime = round(os.path.getmtime(fname)*1000)
        pass
    elif os.path.isdir(fname):
        ftime = round(os.path.getctime(fname)*1000)
        pass
    return True if (ntime-ftime)/(1000*60*60) > hours else False
