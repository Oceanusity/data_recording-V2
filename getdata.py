import multiprocessing 
import time
import subprocess
import sys
import os
from subprocess import call
from autoping import ip_list_get as list_get
from allrate import ddate_recording
import loopdownload
import allrate
import autoping

if __name__ == '__main__':

    ip_dir = {}
    d_tmp_dir = {}
    ip_dir = list_get('pinglist.txt')         #doc in the dir working now
    d_tmp_dir = list_get('dlist.txt')

    process_ping = len(ip_dir)
    process_d = len(d_tmp_dir)
    if process_d == 0 or process_ping == 0 :
        if process_d == 0 :
            print('missing download mission')
            exit()
        else :
            print('missing ping mission')
            exit()

    process_num = process_d + process_ping
    pool = multiprocessing.Pool(processes = process_num)

    t = multiprocessing.Process( target = ddate_recording ,args = ("ddata",))
    t.daemon = True
    t.start()


    try:
        for ip , filename in ip_dir.items():
            pool.apply_async( func = autoping.start , args = (0,ip,filename) )
        for url , tmp_file in d_tmp_dir.items():
            pool.apply_async( func = loopdownload.check_and_go , args = (url,tmp_file) )
        pool.close()
        pool.join()
    except:
        KeyboardInterrupt

