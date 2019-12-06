# encoding: utf-8

##############################################################################
#   Function: 任务线程                            #
#   Author:                                               #
#   Date:                                                         #
##############################################################################

import threading
import time
import os
import logging

from file.clean import get_conf
from file.clean.fileutils import *
#from file.clean import CleanError

fctime = lambda : time.strftime("%m/%d/%Y %H:%M:%S", time.localtime())
fstime = lambda st_time: time.strftime("%Y%m%d%H%M%S", time.localtime(st_time))
curfday  = lambda : time.strftime("%m/%d/%Y", time.localtime())

class ScanTask(threading.Thread):

    def __init__(self, name, cpath="", exit=False):
        threading.Thread.__init__(self)
        threading.Thread.setName(self,name)
        #self.__path = cpath
        self.__path = cpath if cpath !="" else get_conf('clean_path',None)
        self.__filetype = get_conf('clean_type',None)
        self.__expire = int(get_conf('expire_day',7))
        self.__interval = int(get_conf('sleep_interval',60))
        self.__delEmpdir = get_conf('del_empty_dir', False)
        self.__exit = exit
        self.reset()

    def reset(self):
        self.day_flag = curfday()
        self.day_files = 0
        self.day_folders = 0
        self.day_fails = 0

    def exit(self): self.__exit = True

    def run(self):
        logging.info("starting %s with interval=%s, expire=%s, path=%s" % (self.getName(), self.__interval, self.__expire,self.__path))
        type_set = eval(self.__filetype)
        loop_flg = False
        while not loop_flg:
            cur_files, cur_folders, cur_fails = (0,0,0)
            if self.day_flag != curfday():
                self.reset()

            if not exists(self.__path):
                logging.info("cur loop scan not exists path {0}".format(self.__path))
                time.sleep(self.__interval)
                break
            try:
                dir_level1 = 1
                for root, dirs, files in os.walk(self.__path,topdown=True, onerror=None, followlinks=False):
                    #print "current loop find expire file " + str(len(files))
                    ##############################################################################
                    for file in files:
                        fname = os.path.join(root,file)
                        if istype(fname, type_set) and expire(fname, 24*self.__expire):
                            try:
                                mtime = smtime(fname)
                                dflag = rmfile(fname)
                                logging.info('''delete file[{0}][{1}] {2}'''.format(dflag, fstime(mtime), fname))
                                cur_files += 1
                            except Exception as re:
                            #except CleanError as re:
                                logging.warning(re)
                                cur_fails += 1
                                continue
                    ##############################################################################
                    if str(root) == self.__path:
                        #skip root folder
                        pass
                    elif isempty(root) and self.__delEmpdir==True: # expire(root, 24*self.__expire):
                        try:
                            mcime = sctime(root)
                            dflag = rmdirs(root)
                            logging.info('''delete folder[{0}][{1}] {2}'''.format(dflag, fstime(mcime), str(root)))
                            cur_folders += 1
                        #except CleanError as re:
                            #logging.warning(re.message)
                        except Exception as re:
                            logging.warning(re)
                            cur_fails += 1
                            continue
                    else:
                        #print "current loop find expire folder 0"
                        pass
                    ##############################################################################
            except:
                logging.error(traceback.print_exc())
                continue
            finally:
                    self.day_files += cur_files
                    self.day_folders += cur_folders
                    self.day_fails += cur_fails
                    logging.info("cur loop delete expire file {0} ,folder {1} ,fail {2}".format(cur_files,cur_folders,cur_fails))
                    logging.info("day loop delete expire file {0} ,folder {1} ,fail {2}".format(self.day_files,self.day_folders,self.day_fails))
                    if self.__exit:
                        loop_flg = True
                    else:
                        logging.info("{0} sleep {1}s".format(self.getName(),self.__interval))
                        time.sleep(self.__interval)

        #Exiting
        logging.info("exiting thread[%s] at %s" % (self.getName(), fctime()))
