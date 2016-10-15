import subprocess
import os
import glob, json, time, codecs
from socketIO_client import SocketIO, BaseNamespace

server_ip = '192.168.137.2'
action = 'no action'

class Namespace(BaseNamespace):

    def on_aaa_response(self, *args):
        print('on_aaa_response', args)
        self.emit('bbb')
        
def receive_action(*args):
    subprocess.Popen.kill(a)
    subprocess.call(["killall", "feh"])
socketIO = SocketIO(server_ip, 8080, Namespace)        
while True:
    socketIO.on('action', receive_action)
    socketIO.wait(seconds=1)
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
    for i in range(0,len(playlist['assets'])):
            if(playlist['assets'][i]['position'] == 'S'):
                with codecs.open('/home/pi/media/slideShow.txt', 'w', 'utf-8') as f:
                    f.write(playlist['assets'][i]['fileName'])
    
                a = subprocess.Popen(['python', 'slide.py'])
                time.sleep(10)
                subprocess.Popen.kill(a)
                subprocess.call(["killall", "feh"])
