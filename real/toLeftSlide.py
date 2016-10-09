import subprocess
import os
import glob, json, time, codecs

check = False
screen = os.popen("xrandr -q -d :0").readlines()[0]
width = screen.split()[7]
height = screen.split()[9][:-1]
position = ' '
while True:
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
        check=False
    elif(playlist['layout'] == '2a'):
        check=True
            #if check==True:
    for i in range(0,len(playlist['assets'])):
            if(playlist['assets'][i]['position'] == 'S'):
                with codecs.open('/home/pi/media/slideShow.txt', 'w', 'utf-8') as f:
                    f.write(playlist['assets'][i]['fileName'])
    
                a = subprocess.Popen(['python', 'leftSlide.py'])
                time.sleep(10)
                subprocess.Popen.kill(a)
                subprocess.call(["pkill", "-f", playlist['assets'][i]['fileName']])
