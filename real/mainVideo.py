#!/usr/bin/python
import sys, socket
import subprocess
import os
import glob, json, time, codecs

path ='/home/pi/media/'
screen = os.popen("xrandr -q -d :0").readlines()[0]
width = screen.split()[7]
height = screen.split()[9][:-1]
position = ' '
while(1):
    i=0
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
        
    try:
        json_data = open('/home/pi/media/videoShow.json').read()
        fileName = json.loads(json_data)
        #print playlist['assets'][0]['fileName']
    except:
        print "no Media"
            
    listFile = []

    if(playlist['layout'] == '1'):
        if(playlist['ticker']['behavior'] == 'none'):
            position = '0 0 '+str(width)+' '+str(height)
        else:
            position = '0 0 '+str(width)+' '+str(int(float(height)*0.9))
    elif(playlist['layout'] == '2a'):
        if(playlist['ticker']['behavior'] == 'none'):
            position = '0 0 '+str(int(float(width)*0.75))+' '+str(height)
        else:
            position = '0 0 '+str(int(float(width)*0.75))+' '+str(float(height)*0.9)
    elif(playlist['layout'] == '2b'):
        if(playlist['ticker']['behavior'] == 'none'):
            position = "%d %d %d %d" % (int(float(width)*0.25), 0, int(width), int(height))
        else:
            position = "%d %d %d %d" % (int(float(width)*0.25), 0, int(width), int(float(height)*0.9))
    elif(playlist['layout'] == '3a'):
        if(playlist['ticker']['behavior'] == 'none'):
            position = "%d %d %d %d" % (0, int(float(height)*0.2), int(width), int(height))
        else:
            position = "%d %d %d %d" % (0, int(float(height)*0.2), int(width), int(float(height)*0.9))
    elif(playlist['layout'] == '3b'):
        if(playlist['ticker']['behavior'] == 'none'):
            position = "%d %d %d %d" % (0, 0, int(width), int(float(height)*0.8))
        else:
            position = "%d %d %d %d" % (0, 0, int(width), int(float(height)*0.7))
        #position = '0 0 '+str(int(float(width)*0.75))+' '+str(height)
        

    if(playlist['ticker']['behavior'] == 'none'):
        if(fileName['format'] == 'file'):
            a = subprocess.call( [ "omxplayer", "--win", position, "-o", "hdmi", '/home/pi/media/'+fileName['name']])
        else:
            a = subprocess.call( [ "omxplayer", "--win", position, "-o", "hdmi", fileName['name']])
            
    

