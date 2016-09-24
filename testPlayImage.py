#!/usr/bin/python
import sys
import subprocess
import os
import glob, json, time, codecs
from threading import Timer
path ='/home/pi/media/'

def __print():
    subprocess.Popen.kill(a)
    a.wait()
with codecs.open('/home/pi/media/imageShow.txt', 'w', 'utf-8') as f:
    f.write("t3.jpg")
    
a = subprocess.Popen(["python", 'testImageLoop.py'])

time.sleep(3)
subprocess.Popen.kill(a)
subprocess.call(["killall", "feh"])
print "end"
      

