import os
import time
import fnmatch
import sys
from subprocess import call
from threading import Thread

def clean(filename):
    workdir = os.getcwd()
    fullname = os.path.join(workdir,filename)
    if os.path.exists(fullname):
        for videoname in os.listdir(fullname):
            print videoname
            if videoname.endswith("mp4") or videoname.endswith("flv"):
                if os.path.getsize(os.path.join(fullname,videoname)) > 1000 :
                    os.remove(os.path.join(fullname,videoname))
            elif videoname.endswith("xml"):         #to clean the annoying .cmt.xml doc
                os.remove(os.path.join(fullname,videoname))
    else :
        print "dir not exits"

def check_and_go(args):
    try:
        if not (args[0] and args[1]):
            usage_tip(0)
        if "index" in args[0]:
            usage_tip(2)
        else:
             download_loop(args[0],args[1])
    except IndexError:
        usage_tip(0)
    except ValueError:
        usage_tip(1)

def download_loop(link,filename):
    try:
        while True:
            print("Start downloading...%s\nfilename=%s\n" % (link,filename))
            call( "you-get -d " + link  +" -o " + filename, shell=True)
            time.sleep(10)         
            clean(filename)
    except:
        KeyboardInterrupt

def usage_tip(exit_flag):
    if exit_flag == 0:
        print("Missing parameters !\n")
    else:
        print("Please check you parameters !\n")
    print("Usage: python download_loop.py [PageLink][filename]")
    print("Example: python download_loop.py http://www.bilibili.com/video/av4432868/ ./tmp/bb ")
    sys.exit(exit_flag)

if __name__ == "__main__":
    check_and_go(sys.argv[1:])
