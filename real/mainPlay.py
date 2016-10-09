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
            position = "%d %d %d %d" % (int(float(width)*0.25), 0, int(width), height)
        else:
            position = "%d %d %d %d" % (int(float(width)*0.25), 0, int(width), int(float(height)*0.9))
    elif(playlist['layout'] == '3a'):
        if(playlist['ticker']['behavior'] == 'none'):
            position = "%d %d %d %d" % (0, int(float(height)*0.2), int(width), height)
        else:
            position = "%d %d %d %d" % (0, int(float(height)*0.2), int(width), int(float(height)*0.9))
    elif(playlist['layout'] == '3b'):
        if(playlist['ticker']['behavior'] == 'none'):
            position = "%d %d %d %d" % (0, 0, int(width), int(float(height)*0.8))
        else:
            position = "%d %d %d %d" % (0, 0, int(width), int(float(height)*0.7))
        #position = '0 0 '+str(int(float(width)*0.75))+' '+str(height)
        

    
    if(playlist['ticker']['behavior'] == 'none'):
        for i in range(0,len(playlist['assets'])):
            if(playlist['assets'][i]['position'] == 'M'):
                listFile.insert(0, playlist['assets'][i]['fileName'])
            print 'playing' + playlist['assets'][i]['fileName']

            if(playlist['assets'][i]['type'] == 'video'):
                if(playlist['assets'][i]['format'] == 'file'):
                    a = subprocess.call( [ "omxplayer", "--win", position, "-o", "hdmi", '/home/pi/media/'+playlist['assets'][i]['fileName']])
                else:
                    a = subprocess.call( [ "omxplayer", "--win", position, "-o", "hdmi", playlist['assets'][i]['fileName']])
            elif(playlist['assets'][i]['type'] == 'image' and playlist['assets'][i]['position'] == 'M'):
                with codecs.open('/home/pi/media/imageShow.txt', 'w', 'utf-8') as f:
                    f.write(playlist['assets'][i]['fileName'])
                    
                if(playlist['assets'][i]['format'] == 'file'):
                    a = subprocess.Popen(["python", 'testImageLoop.py'])
                else:
                    a = subprocess.Popen(["python", 'testImageLoop.py'])
                time.sleep(30)
                subprocess.Popen.kill(a)
                subprocess.call(["killall", "feh"])
    else:
        for i in range(0,len(playlist['assets'])):
            listFile.insert(0, playlist['assets'][i]['fileName'])
            print 'playing' + playlist['assets'][i]['fileName']

            if(playlist['assets'][i]['type'] == 'video'):
                if(playlist['assets'][i]['format'] == 'file'):
                    a = subprocess.call( [ "omxplayer", "--win", position, "-o", "hdmi", '/home/pi/media/'+playlist['assets'][i]['fileName']])
                else:
                    a = subprocess.call( [ "omxplayer", "--win", position, "-o", "hdmi", playlist['assets'][i]['fileName']])
            elif(playlist['assets'][i]['type'] == 'image' and playlist['assets'][i]['position'] == 'M' ):
                with codecs.open('/home/pi/media/imageShow.txt', 'w', 'utf-8') as f:
                    f.write(playlist['assets'][i]['fileName'])
                    
                if(playlist['assets'][i]['format'] == 'file'):
                    a = subprocess.Popen(["python", 'mainImage.py'])
                else:
                    a = subprocess.Popen(["python", 'mainImage.py'])
                time.sleep(20)
                subprocess.Popen.kill(a)
                subprocess.call(["killall", "feh"])
            
    #print listFile
            
    for infile in listFile:
        print infile
        

