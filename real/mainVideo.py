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
        json_data = open('/home/pi/media/schedule_playlist_control.json').read()
        control = json.loads(json_data)
    except:
        try:
            json_data = open('/home/pi/media/control.json').read()
            control = json.loads(json_data)
            #print control['control']['playlist']
        except:
            print "mainVideo No Control"

    try:
        json_data = open('/home/pi/media/'+control['control']['playlist']+'.json').read()
        playlist = json.loads(json_data)
        #print playlist['assets'][0]['fileName']
    except:
        print "mainVideo no Media"
        
    try:
        json_data = open('/home/pi/media/videoShow.json').read()
        fileName = json.loads(json_data)
        #print playlist['assets'][0]['fileName']
    except:
        print "mainVideo no show"
            
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

    pathFile = ' '
    if(fileName['type'] == 'youtube'):
        pathFile = open('/home/pi/media/'+fileName['name']).read()
        command = "youtube-dl -g -f best %s" % pathFile
        yt = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        pathFile, err = yt.communicate()
        pathFile = pathFile.rstrip()
        print pathFile
    elif(fileName['type'] == 'other'):
        pathFile = open('/home/pi/media/'+fileName['name']).read()

    if(fileName['format'] == 'file' and fileName['type'] == 'video'):
        pathFile = '/home/pi/media/'+fileName['name']
    elif(fileName['format'] == 'url' and fileName['type'] == 'video'):
         pathFile = fileName['name']
    

    
    if(fileName['format'] == 'file'):
        a = subprocess.call( [ "omxplayer", "--win", position, "-o", "both", pathFile])
    else:
        a = subprocess.call( [ "omxplayer", "--win", position, "-o", "both", pathFile])
            
    

