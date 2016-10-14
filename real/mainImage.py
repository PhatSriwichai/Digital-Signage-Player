#!/usr/bin/python
import sys
import subprocess
import os
import glob, json, time, codecs
from threading import Timer
path ='/home/pi/media/'
screen = os.popen("xrandr -q -d :0").readlines()[0]
width = screen.split()[7]
height = screen.split()[9][:-1]
position = ''

try:
    json_data = open('/home/pi/media/schedule_playlist_control.json').read()
    control = json.loads(json_data)
except:
    try:
        json_data = open('/home/pi/media/control.json').read()
        control = json.loads(json_data)
        #print control['control']['playlist']
    except:
        print "mainImage No Control"

try:
    json_data = open('/home/pi/media/'+control['control']['playlist']+'.json').read()
    playlist = json.loads(json_data)
    #print playlist['assets'][0]['fileName']
except:
    print "no Media"

if(playlist['layout'] == '1'):
    fileName = open('/home/pi/media/imageShow.txt').read()
    if(playlist['ticker']['behavior'] == 'none'):
        a = subprocess.call( [ "feh", "-F", '/home/pi/media/'+fileName])
    else:
        position = "%dx%d+%d+%d" % (int(width), int(float(height)*0.87), 0, 0)
    a = subprocess.call( [ "feh", "-B", "black", "-x", "-g", position, '/home/pi/media/'+fileName])
    
elif(playlist['layout'] == '2a'):
    if(playlist['ticker']['behavior'] == 'none'):
        #position = str(width-int(float(width)*0.75))+'x'+str(height)+'+'+str(int(float(width)*0.75))+'+0'
        position = "%dx%s+%d+%d" % (int(width)-int(float(width)*0.25), height, 0, 0)
    else:
        position = "%dx%d+%d+%d" % (int(width)-int(float(width)*0.25), int(float(height)*0.87), 0, 0)
elif(playlist['layout'] == '2b'):
    if(playlist['ticker']['behavior'] == 'none'):
        #position = str(width-int(float(width)*0.75))+'x'+str(height)+'+'+str(int(float(width)*0.75))+'+0'
        position = "%dx%d+%d+%d" % (int(width)-int(float(width)*0.25), int(height), int(float(width)*0.25), 0)
    else:
        position = "%dx%d+%d+%d" % (int(width)-int(float(width)*0.25), int(float(height)*0.87), int(float(width)*0.25), 0)
elif(playlist['layout'] == '3a'):
    if(playlist['ticker']['behavior'] == 'none'):
        #position = str(width-int(float(width)*0.75))+'x'+str(height)+'+'+str(int(float(width)*0.75))+'+0'
        position = "%dx%d+%d+%d" % (int(width), int(float(height)*0.8), 0, int(float(height)*0.2))
    else:
        position = "%dx%d+%d+%d" % (int(width), int(float(height)*0.7), 0, int(float(height)*0.2))
elif(playlist['layout'] == '3b'):
    if(playlist['ticker']['behavior'] == 'none'):
        #position = str(width-int(float(width)*0.75))+'x'+str(height)+'+'+str(int(float(width)*0.75))+'+0'
        position = "%dx%d+%d+%d" % (int(width), int(float(height)*0.8), 0, 0)
    else:
        position = "%dx%d+%d+%d" % (int(width), int(float(height)*0.7), 0, 0)
        


fileName = open('/home/pi/media/imageShow.txt').read()
a = subprocess.call( [ "feh", "-B", "black", "-x", "-g", position, '/home/pi/media/'+fileName])

      

