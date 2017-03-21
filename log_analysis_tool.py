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

threads = []
decode_time_list=[]
swap_time_list=[]
updateTexture_time_list=[]

#analysis log file name
file_name = str(sys.argv[1])
print "file_name = %s" %file_name


#show the frame count in figure
show_frame_start = 50
show_frame_count = 300


def process(filename):    
    file = open(filename,"r")
    decode_line = 0
    render_line = 0
    update_line = 0
    for eachline in file.readlines():
        index0 = eachline.find('avcodec_decode_video2')
        index1 = eachline.find('SDL_RenderPresent')
        index2 = eachline.find('SDL_UpdateTexture')
        if index0 != -1:
            str = eachline.split("[")[1].split("]")[0]
            time = int(str)  
            decode_time_list.append(time)
            decode_line += 1
            print "decode: %s ms" %str
        elif index1 != -1:
            str = eachline.split("[")[1].split("]")[0]
            time = int(str)
            swap_time_list.append(time)
            print "swap  : %s ms" %str
        elif index2 != -1:
            str = eachline.split("[")[1].split("]")[0]
            time = int(str)  
            updateTexture_time_list.append(time)
            print "draw  : %s ms" %str
    
    print "decoding frame count: %d" %(len(decode_time_list))


def drawBar(arr, des):
    if show_frame_count != -1 :
        count = show_frame_count
    else :
        count = len(arr)
    print "frame count = %d" %count
    X = np.arange(count)   
    Y = arr[show_frame_start:show_frame_start + count]#arr
    fig = plt.figure()
    bar_width = 1.0
    text_hight = 1
    plt.bar(X, Y, bar_width, color="red", edgecolor = 'white')
    #plt.text(X, Y + text_hight, '%d' %Y, ha='center', va= 'bottom')
    
    plt.xlabel("frame count")
    y_str = "time consuming (ms)";
    plt.ylabel(y_str)    
    
    title_str = des + ":" +y_str + ":Frame count:" + str(count);
    plt.title(title_str)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.03), fancybox=True, ncol=5)
    plt.show()


t1 = threading.Thread(target=drawBar,args=(decode_time_list,"Decoding",))
threads.append(t1)
t2 = threading.Thread(target=drawBar,args=(swap_time_list,"SwapBuffer",))
threads.append(t2)
t3 = threading.Thread(target=drawBar,args=(updateTexture_time_list, "UpdateTexture",))
threads.append(t3)

if __name__ == '__main__':
    process(file_name);
   
    drawBar(decode_time_list,"Decoding");    
    drawBar(swap_time_list,"SwapBuffer");
    drawBar(updateTexture_time_list,"UpdateTexture");

    #for t in threads:
    #    t.setDaemon(False)
    #    t.start()
    #    print "thread ------started"
    
