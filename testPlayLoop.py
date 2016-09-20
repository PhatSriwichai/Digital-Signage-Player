#!/usr/bin/python
import sys
import subprocess
import os
import glob, json
path ='/home/pi/media/'
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
    for i in range(0,len(playlist['assets'])):
        listFile.insert(0, playlist['assets'][i]['fileName'])
        print 'playing' + playlist['assets'][i]['fileName']
        if(playlist['assets'][i]['format'] == 'file'):
            a = subprocess.call( [ "omxplayer", "-o", "both", "-b", '/home/pi/media/'+playlist['assets'][i]['fileName']])
        else:
            a = subprocess.call( [ "omxplayer", "-o", "both", "-b", playlist['assets'][i]['fileName']])
    #print listFile
            
    for infile in listFile:
        print infile
        

