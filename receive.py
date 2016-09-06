import fcntl, socket, struct
import base64, StringIO, sys
from socketIO_client import SocketIO, BaseNamespace
from PIL import Image
from io import BytesIO
import time
import cv2
import os

server_ip = '192.168.137.2'

class Namespace(BaseNamespace):

    def on_aaa_response(self, *args):
        print('on_aaa_response', args)
        self.emit('bbb')
        
def receive_check_file(*args):
    listFile = os.listdir("/home/pi/media")
    
    i = 0;
    for inputt in args[0]:
        print args
        i = i + 1
        if any(inputt in l for l in listFile):
            continue;
        package = [inputt, mac]
        socketIO.emit('route', 'file')
        socketIO.wait(seconds=1)
        socketIO.emit('file', package)
        socketIO.wait(seconds=1)
    print i
        
        
    
def receive_file(*args):
    if(args[2] == 'jpg' or args[2] == 'png'):
        print "receiving image"
        imageData = args[1].encode('latin-1')
        imageName = args[0].encode('utf-8')
        im = Image.open(BytesIO((imageData)))
        im.save('/home/pi/media/'+imageName,'JPEG')
    else:
        print "receiving video"
        videoData = args[1].encode('latin-1')
        videoName = args[0].encode('utf-8')
        with open('/home/pi/media/'+videoName, 'wb') as vi:
            vi.write(videoData)
        cap = cv2.VideoCapture('/home/pi/media/'+videoName)
        success, frame = cap.read()
        print success
    print('success')

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])
    
socketIO = SocketIO(server_ip, 8080, Namespace)
mac = getHwAddr('eth0')

#while True:
socketIO.on(mac+"_check", receive_check_file)
socketIO.wait(seconds=1)
socketIO.on(mac, receive_file)
socketIO.wait(seconds=1) 
socketIO.wait() 
