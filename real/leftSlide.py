#!/usr/bin/python
import sys
import subprocess
import os
import glob, json, time, codecs
path ='/home/pi/media/'

screen = os.popen("xrandr -q -d :0").readlines()[0]
width = screen.split()[7]
height = screen.split()[9][:-1]
position = ' '

try:
    json_data = open('/home/pi/media/control.json').read()
    control = json.loads(json_data)
    #print control['control']['playlist']
except:
    print "No Control"

try:
    json_data = open('/home/pi/media/'+control['control']['playlist']+'.json').read()
    playlist = json.loads(json_data)
    #print playlist['assets'][0]['fileName']
except:
    print "no Media"


if(playlist['layout'] == '1'):
    print 'a'
elif(playlist['layout'] == '2a'):
    if(playlist['ticker']['behavior'] == 'none'):
        #position = str(width-int(float(width)*0.75))+'x'+str(height)+'+'+str(int(float(width)*0.75))+'+0'
        position = "%dx%s+%d+%d" % (int(width)-int(float(width)*0.75), height, int(float(width)*0.75), 0)
    else:
        position = "%dx%d+%d+%d" % (int(width)-int(float(width)*0.75), int(float(height)*0.9), int(float(width)*0.75), 0)
elif(playlist['layout'] == '2b'):
    if(playlist['ticker']['behavior'] == 'none'):
        #position = str(width-int(float(width)*0.75))+'x'+str(height)+'+'+str(int(float(width)*0.75))+'+0'
        position = "%dx%s+%d+%d" % (int(width)-int(float(width)*0.75), height, 0, 0)
    else:
        position = "%dx%d+%d+%d" % (int(width)-int(float(width)*0.75), int(float(height)*0.9), 0, 0)
elif(playlist['layout'] == '3a'):
    if(playlist['ticker']['behavior'] == 'none'):
        #position = str(width-int(float(width)*0.75))+'x'+str(height)+'+'+str(int(float(width)*0.75))+'+0'
        position = "%dx%s+%d+%d" % (int(width), int(float(height)*0.2), 0, 0)
    else:
        position = "%dx%s+%d+%d" % (int(width), int(float(height)*0.2), 0, 0)
elif(playlist['layout'] == '3b'):
    if(playlist['ticker']['behavior'] == 'none'):
        position = "%dx%s+%d+%d" % (int(width), int(float(height)*0.2), 0, int(float(height)*0.8))
    else:
        position = "%dx%d+%d+%d" % (int(width), int(float(height)*0.2), 0, int(float(height)*0.7))  
fileName = open('/home/pi/media/slideShow.txt').read()
a = subprocess.call( [ "feh", "-B", "black", "-x", "-g", position, '/home/pi/media/'+fileName])
