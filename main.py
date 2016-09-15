import os, subprocess, sys
import socket
import time
from socketIO_client import SocketIO, BaseNamespace

server_ip = '192.168.137.2'
action = 'no action'

class Namespace(BaseNamespace):

    def on_aaa_response(self, *args):
        print('on_aaa_response', args)
        self.emit('bbb')

def receive_action(*args):
    #print args[0]
    if(args[0] == 'play'):
        subprocess.Popen.kill(play)
        subprocess.call(["killall", "omxplayer"])
        subprocess.call(["killall", "/usr/bin/omxplayer.bin"])
        time.sleep(1)
        global play
        play = subprocess.Popen(["python", "testPlayLoop.py"])
        time.sleep(1)
    #elif(args[0] == 'play'):
        


socketIO = SocketIO(server_ip, 8080, Namespace)
play = subprocess.Popen(["python", "testPlayLoop.py"], shell=False)
#time.sleep(5)
#subprocess.Popen.kill(play)
#subprocess.call(["killall", "/usr/bin/omxplayer.bin"])

receive = subprocess.Popen(["python", "receive.py"])
on_off = subprocess.Popen(["python", "on_off.py"])

socketIO.on('action', receive_action)
socketIO.wait()
#while(1):
    
    #socketIO.on('action', receive_action)
    #socketIO.wait(seconds=1)
