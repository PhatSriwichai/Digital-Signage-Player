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
x = 0
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
            print "mainPlay No Control"

    try:
        json_data = open('/home/pi/media/'+control['control']['playlist']+'.json').read()
        playlist = json.loads(json_data)
        #print playlist['assets'][0]['fileName']
    except:
        print "mainPlay no Media"
            
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
        

    
    
    for i in range(0,len(playlist['assets'])):
        
        if(playlist['assets'][i]['position'] == 'M'):
            listFile.insert(0, playlist['assets'][i]['fileName'])
        print 'playing ' + playlist['assets'][i]['fileName']
        pathFile = ' '
        if(playlist['assets'][i]['type'] != 'image'):
            if(playlist['assets'][i]['type'] == 'youtube'):
                pathFile = open('/home/pi/media/'+playlist['assets'][i]['fileName']).read()
                command = "youtube-dl -g -f best %s" % pathFile
                yt = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                pathFile, err = yt.communicate()
                pathFile = pathFile.rstrip()
                #pathFile = subprocess.check_output(["youtube-dl", "-g", "-f", "best", open('/home/pi/media/'+playlist['assets'][i]['fileName']).read()])
            elif(playlist['assets'][i]['type'] == 'other'):
                pathFile =  open('/home/pi/media/'+playlist['assets'][i]['fileName']).read()

            if(playlist['assets'][i]['format'] == 'file' and playlist['assets'][i]['type'] == 'video'):
                pathFile = '/home/pi/media/'+playlist['assets'][i]['fileName']
            elif(playlist['assets'][i]['format'] == 'url' and playlist['assets'][i]['type'] == 'video'):
                pathFile = playlist['assets'][i]['fileName']
    
                    
            timesec = int(playlist['assets'][i]['time'])
            if(timesec == -1):
                print pathFile
                a = subprocess.call( [ "omxplayer", "--win", position, "-o", "both", pathFile])
            else:
                if(playlist['assets'][i]['type'] == 'youtube'):
                    timesec = timesec+10
                fileName = {}
                fileName['name'] = playlist['assets'][i]['fileName']
                fileName['format'] = playlist['assets'][i]['format']
                fileName['type'] = playlist['assets'][i]['type']
                json_data = json.dumps(fileName)
                j = json.loads(json_data)
                with codecs.open('/home/pi/media/videoShow.json', 'w', 'utf-8') as f:
                    f.write(json.loads(json.dumps(json_data, indent=2, sort_keys = True,ensure_ascii=False, separators=(',',':'))))
                a = subprocess.Popen(["python", 'mainVideo.py'])
                time.sleep(timesec)
                subprocess.Popen.kill(a)
                subprocess.call(["killall", "omxplayer"])
                subprocess.call(["killall", "/usr/bin/omxplayer.bin"])
                    
        elif(playlist['assets'][i]['type'] == 'image' and playlist['assets'][i]['position'] == 'M'):
            with codecs.open('/home/pi/media/imageShow.txt', 'w', 'utf-8') as f:
                f.write(playlist['assets'][i]['fileName'])
            x = x + 1      
            if(playlist['assets'][i]['format'] == 'file'):
                a = subprocess.Popen(["python", 'mainImage.py'])
            else:
                a = subprocess.Popen(["python", 'mainImage.py'])
            timesec = int(playlist['assets'][i]['time'])
            if(x==1):
                timesec = 3
            else:
                if(timesec == -1):
                    timesec = 60
                
            time.sleep(timesec)
            subprocess.Popen.kill(a)
            subprocess.call(["pkill", "-f", playlist['assets'][i]['fileName']])
    
               

