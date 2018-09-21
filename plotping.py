import os
import re
import sys
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

def in_the_range(datetime,begin_time,end_time):
    if begin_time < datetime < end_time :
        return True
    else:
        return False
        
def ave_speed(scale,tmp_x_time,tmp_y_data,x_time,y_data):
    return True

def read_data(doc,begin_time,end_time):
    pattern_delaytime_str = 'time=(([0-2]\d)|3[0-5]).\d+' #delay_time below 100 ms
    pattern_delaytime_num = '(([0-2]\d)|3[0-5]).\d+'
    pattern_datetime = '(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Oct|Nov|Dec)\s+([1-9]|[1-2]\d|3[0-1])\s+([0-1]\d|2[0-4]):[0-6]\d:\d{2}'
    bool = 0
    tmp_x_time = []
    tmp_y_data = []
    with open(doc,'r') as f:
        tmp_data = []
        tmp_str = ""
        for line in f.readlines():
            if bool == 0:
                if re.search(pattern_datetime,line):
                    tmp_time =  datetime.strptime(re.search(pattern_datetime,line).group() ,"%b %d %H:%M:%S")
                    if in_the_range(tmp_time,begin_time,end_time):
                        bool = 1
                        continue
        
            if bool == 1:
                if re.search(pattern_delaytime_str,line):
                    tmp_data.append(float(re.search(pattern_delaytime_num,re.search(pattern_delaytime_str,line).group()).group()))
                elif re.search(pattern_datetime,line):
                    tmp_time = datetime.strptime(re.search(pattern_datetime,line).group() ,"%b %d %H:%M:%S")
                    if in_the_range(tmp_time,begin_time,end_time):
                            sum = 0
                            num = 0
                            while len(tmp_data) > 0:
                                delay = tmp_data.pop()
                                sum += delay
                                num += 1
                            if num != 0 :             #in the vitual machine in this computer, it need to update
                                average = sum / num
                                if average < 35:
                                    tmp_x_time.append(tmp_time)   
                                    tmp_y_data.append(average)
                    else:
                        bool = 0
                        continue
    return tmp_x_time,tmp_y_data

if __name__ == '__main__':

    if len(sys.argv) < 6:
        print("missing parameters \n example : python plotping.py pingdata 7-03 10:30:00 7-04 11:40:00") # the 0 in day is required
        exit()
    #judge the right formation of datetime 
    doc = sys.argv[1]
    begin_time = datetime.strptime(sys.argv[2] + sys.argv[3], "%m-%d%H:%M:%S")  
    end_time = datetime.strptime(sys.argv[4] + sys.argv[5], "%m-%d%H:%M:%S")

    scale = 5      #the time scale for the ave_speed(min)
    tmp_x_time = []
    tmp_y_data =[]
    x_time =[]
    y_data = []

    tmp_x_time,tmp_y_data = read_data(doc,begin_time,end_time)

    ave_speed(scale,tmp_x_time,tmp_y_data,x_time,y_data)

    #can be changed to x_time after the ave_speed is finished
    major_fmt = mdates.DateFormatter('%m-%d %H')
    minor_fmt = mdates.DateFormatter('%M')
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(major_fmt)
    #plt.gca().xaxis.set_minor_locator(mdates.MinuteLocator(interval=10))
    #plt.gca().xaxis.set_minor_formatter(minor_fmt)
    #the former two lines is not need
    plt.xlim(begin_time,end_time)
    plt.scatter(tmp_x_time,tmp_y_data,s=1,alpha=0.5)
    plt.gcf().autofmt_xdate()  # rotate the locator
    plt.show()    
