#!/usr/bin/python
'''
calucate the rate of download video from bb qq ...
the method  is
pre : previous size of dir eg tmp/qq
now : now size of dir eg tmp/qq
rate : (now - pre) / 5
'''
#cal all the doc in the tmp dir and tmp must in the 
import os
import time
import fnmatch
import sys
def dirsize(path):
    size = 0
    for root,dirnames,filenames in os.walk(path):
        for filename in filenames:
            size = size + os.path.getsize(os.path.join(root,filename))
    return size

def cal(path,pre):
    now = dirsize(path)
    return now, (now - pre) / 5

def ddata_recording(args):

    datafile = ""
    if len(args) == 0 :
        print("missing parameter")
        exit()
    datafile = args[0]
    workdir = os.path.join(os.getcwd(),"./tmp") #can be changed to input by keyboard
    datadir = os.path.join(os.getcwd(),datafile)

    presize = [0 for x in range(0, 20)]
    nowsize = [0 for x in range(0, 20)]     #max<20 init the array 0
    count = 0

    for document in os.listdir(workdir):  
        presize[count] = dirsize(os.path.join( workdir , document))
        count = count + 1

    try:
        while True:
            count = 0
            for document in os.listdir( workdir ): 
                f = open( datafile + '/' + document ,"a+" )
                path = os.path.join( workdir , document )
                t = time.strftime("%m-%d %H:%M:%S", time.localtime())
                nowsize[count] , rate = cal( path , presize[count] )
                if rate > 0 :   #no minus speed here
                    f.write(t + "\n")
                    f.write( document + ":" + str( rate ) + "\n")
                    f.close()
                    presize[count] = nowsize[count]
                    count = count + 1
            time.sleep(5)
    except:
        KeyboardInterrupt

if __name__ == "__main__":
    ddata_recording( sys.argv[1:] )

