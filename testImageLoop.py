#!/usr/bin/python
import sys
import subprocess
import os
import glob, json, time
from threading import Timer
path ='/home/pi/media/'

def __print():
    subprocess,call(["kill", "-9", "%d"%a.pid])
    a.wait()
fileName = open('/home/pi/media/imageShow.txt').read()
a = subprocess.call( [ "feh", "-F", '/home/pi/media/'+fileName])

      

