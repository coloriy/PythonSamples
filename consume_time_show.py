#!/usr/bin/python
#coding:utf-8
#by james

import threading
from time import ctime,sleep
import os
import sys
import string
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

time_list=[]

#analysis log file name
file_name = str(sys.argv[1])
keyword = str(sys.argv[2])
show_count = str(sys.argv[3])
print "file_name = %s" %file_name
print "keyword = %s" %keyword
print "show count = %s" %show_count


#show start index of array in figure
show_start = 5
average_time = 0
def process(filename):    
    file = open(filename,"r")
    text_line = 0
    time_total = 0
    for eachline in file.readlines():
        index = eachline.find(keyword)
        if index != -1:
            str = eachline.split("[")[1].split("]")[0]
            time = int(str)  
            if time > 0:
                time_list.append(time)
                text_line += 1
                time_total += time
                print "time: %s ms" %str
    print "list count: %d" %(len(time_list))
    average_time = time_total/text_line
    print "average time: %d" %(average_time)
    return average_time

def drawBar(arr, des, average_time):
    if int(show_count) == 0:
       count = len(arr) - show_start
    else:
       count = int(show_count)
    print "show start index : %d" %show_start
    print "show total count : %d" %(count-show_start)
    X = np.arange(count) + show_start
    Y = arr[show_start:show_start + count]#arr
    fig = plt.figure()
    bar_width = 1.0
    text_hight = 1
    plt.bar(X, Y, bar_width, color="red", edgecolor = 'white')
    #plt.text(X, Y + text_hight, '%d' %Y, ha='center', va= 'bottom')
    
    plt.xlabel("count")
    y_str = "time(ms)"
    plt.ylabel(y_str)    
    
    title_str = des + ":" +y_str + " start index: " + str(show_start) + ", show count: " + str(count) + ", average: " + str(average_time)+ " ms"
    plt.title(title_str)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.03), fancybox=True, ncol=5)
    plt.show()


if __name__ == '__main__':
    average_time = process(file_name);
   
    drawBar(time_list,"time", average_time);
