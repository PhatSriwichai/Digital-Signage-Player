#!/usr/bin/python
import sys
import subprocess
import os
import glob, json
path ='/home/pi/media/'
while(1):
    i=0
    json_data = open('/home/pi/media/control.json').read()
    control = json.loads(json_data)
    #print control['control']['playlist']
    json_data = open('/home/pi/media/'+control['control']['playlist']+'.json').read()
    playlist = json.loads(json_data)
    #print playlist['assets'][0]['fileName']
    
    listFile = []
    for i in range(0,len(playlist['assets'])):
        listFile.insert(0, playlist['assets'][i]['fileName'])
    #print listFile
    
    for infile in listFile:
        print infile
        a = subprocess.call( [ "omxplayer", "-o", "both", "-b", '/home/pi/media/'+infile])
