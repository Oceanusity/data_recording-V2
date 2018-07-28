#put your ping statcists in the document in order
#ip and the data_doc need to be written in the file named pinglist.txt
from __future__ import print_function
import multiprocessing 
import time
import psutil
import subprocess
import sys
import os
def ip_list_get(ip_list_file):     #changed

    ip_dir = {}
    f = open(ip_list_file, 'r') 

    for line in f.readlines():
        line_array = line.strip().split()
        if len(line_array) == 0 :
            continue
        elif len(line_array) == 2 :
            ip_dir[line_array[0]] = line_array[1]
        else:
            print("filename & hosts is needed for py")
            exit()

    f.close()
    return ip_dir

def ping(ip , filename):

    ping = 'ping -c 4 ' + ip
    f = open(filename, 'a+')

    p = subprocess.Popen(ping,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
    )

    result = p.stdout.read()
    time = 'date'
    p  = subprocess.Popen(time,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=True
                         )
    result = result + p.stdout.read()
    '''
    cnt = lines(result)
    print (" %s result size = %d" % (ip,cnt))

    if cnt < 6:
        raise Exception("bad ping %s the dst is unreachable or packet loss 100%" % ip)
    else :
        f.write(result)
    '''
    f.write(result)
    f.close()

def start(rescnt , ip , filename):
    if rescnt < 3 :
        try:
            while True:
                ping(ip,filename) 
        except Exception,e:
            print ("exception : " , e)
            time.sleep(60)
            rescnt = rescnt + 1    
            start(rescnt,ip,filename)
        finally:
            print("end process")


if __name__ == '__main__':

    ip_dir = {}
    ip_dir = ip_list_get('pinglist.txt')

    process_num = len(ip_dir)

    if process_num < 1 :
        print("filename & hosts is needed for py")
        exit()

    else:
        pool = multiprocessing.Pool(processes = process_num)
    try:
        for ip , filename in ip_dir.items():
            pool.apply_async(func = start ,args = (0,ip,filename))
        pool.close()
        pool.join()
    except:
        KeyboardInterrupt