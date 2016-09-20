import fcntl, socket, struct
import base64, StringIO, sys
from socketIO_client import SocketIO, BaseNamespace
from PIL import Image
from io import BytesIO
import time, json, codecs
import cv2
import os, subprocess

server_ip = '192.168.137.2'

countFile = 0
i = 0
class Namespace(BaseNamespace):

    def on_aaa_response(self, *args):
        print('on_aaa_response', args)
        self.emit('bbb')
        
def receive_control_file(*args):
    data = {}
    playlist = {}
    playlist['playlist'] = args[0]
    data['control'] = playlist
    json_data = json.dumps(data)
    j = json.loads(json_data)
    with codecs.open('/home/pi/media/control.json', 'w', 'utf-8') as f:
        f.write(json.loads(json.dumps(json_data, indent=2, sort_keys = True,
                ensure_ascii=False, separators=(',',':'))))
    print 'create control json: control.json'
    global i
    i = i + 1
    global countFile
    if(countFile == 0):
        socketIO.emit('action', 'play')
        socketIO.wait(seconds=1)
        
def receive_check_file(*args):
    print args
    listFile = os.listdir("/home/pi/media")
    data = []
    playlist = {}
    i=0;
    global countFile
    countFile = 0
    
    for inputt in args[0][0]:
        if any(inputt in l for l in listFile):
            continue;
        countFile = countFile+1
    print "CountFile = %d check_file" % countFile
    pack = []

    k=0
    for inputt in args[0][0]:
        print "input = "+inputt
        fileName = {}
        form = {}
        fileName['fileName'] = inputt
        fileName['format'] = args[0][1][k]
        k=k+1
        #data.insert(0, fileName)
        data.insert(0, fileName)
        #data.insert(0, form)
        #print data
        pack.insert(0, data)
        i=i+1
        #print i
        if any(inputt in l for l in listFile):
            continue;
        #countFile = countFile+1
        package = [inputt, mac]
        socketIO.emit('route', 'file')
        socketIO.wait(seconds=1)
        socketIO.emit('file', package)
        socketIO.wait(seconds=1)
        #print "CountFile = %d check_file" % countFile
    playlist['assets'] = data
    #print pack
    json_data = json.dumps(playlist)
    j = json.loads(json_data)
    
    with codecs.open('/home/pi/media/'+args[1]+'.json', 'w', 'utf-8') as f:
        f.write(json.loads(json.dumps(json_data, indent=2, sort_keys = True,
                ensure_ascii=False, separators=(',',':'))))
    print 'create json: '+args[1]+'.json'
    
        
        
    
def receive_file(*args):
    if(args[2] == 'jpg' or args[2] == 'png' or args[2] == 'gif'):
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
    global countFile
    countFile = countFile-1
    print "CountFile = %d receive_file" % countFile
    if(countFile == 0):
        socketIO.emit('action', 'play')
        socketIO.wait(seconds=1)

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])
    
socketIO = SocketIO(server_ip, 8080, Namespace)
mac = getHwAddr('eth0')
print mac



#while True:
socketIO.on(mac+"_check", receive_check_file)
socketIO.wait(seconds=1)
socketIO.on(mac, receive_file)
socketIO.wait(seconds=1)
socketIO.on(mac+"_control", receive_control_file)
socketIO.wait(seconds=1)
socketIO.wait()
    
       


