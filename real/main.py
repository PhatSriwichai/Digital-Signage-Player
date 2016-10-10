import os, subprocess, sys
import socket, fcntl, struct
import glob, json, time, codecs
from PIL import Image
from io import BytesIO
from socketIO_client import SocketIO, BaseNamespace

server_ip = '192.168.137.2'
server_port = 8080
action = 'no action'


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
    print countFile
    if(countFile == 0):
        socketIO.emit('action', 'play')
        socketIO.wait(seconds=1)
        
def receive_check_file(*args):
    print type(args[0][4][0].encode('utf8'))
    text = args[0][4][0]
    if args[0][4][1] != 'none':
        stringHTML = "<!DOCTYPE html>"
        stringHTML += "<html style=\"height:100%\">"
        stringHTML += "<head>"
        stringHTML += "<meta http-equiv=\"Content-Langauge\" content=\"th\""
        stringHTML += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=window-874\""
        stringHTML += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=tis-620\""
        stringHTML += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\""
        stringHTML += "</head>"
        stringHTML += "<body style=\"height:100%; overflow:hidden; background-color:black\">"
        stringHTML += "<section style=\"height:93%\"></section>"
        stringHTML += "<aside style=\"height:10%\">"
        stringHTML += "<marquee bgcolor=\"#000000\" align=\"bottom\" vspace=0 behavior=\""+args[0][4][1]+"\""
        stringHTML += "direction=\"left\" scollamount=\"20\">"
        stringHTML += "<font color=\"#ffffff\" size=\"6\">"+text+"</font>"
        stringHTML += "</marquee>"
        stringHTML += "</aside>"
        stringHTML += "</body>"
        stringHTML += "</html>"
        with codecs.open('/home/pi/media/ticker/'+args[1]+'_ticker.html', 'w', encoding='utf-8') as f:
            f.write(stringHTML)
    else:
        stringHTML = "<!DOCTYPE html>"
        stringHTML += "<html style=\"height:100%\">"
        stringHTML += "<head>"
        stringHTML += "<meta http-equiv=\"Content-Langauge\" content=\"th\""
        stringHTML += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=window-874\""
        stringHTML += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=tis-620\""
        stringHTML += "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\""
        stringHTML += "</head>"
        stringHTML += "<body style=\"height:100%; overflow:hidden; background-color:black\">"
        stringHTML += "<section style=\"height:93%\"></section>"
        stringHTML += "<aside style=\"height:10%\">"
        stringHTML += "<marquee align=\"bottom\" vspace=0 behavior=\"scoll\""
        stringHTML += "direction=\"left\" scollamount=\"20\">"
        stringHTML += "<font size=\"6\"></font>"
        stringHTML += "</marquee>"
        stringHTML += "</aside>"
        stringHTML += "</body>"
        stringHTML += "</html>"
        with codecs.open('/home/pi/media/ticker/'+args[1]+'_ticker.html', 'w', encoding='utf-8') as f:
            f.write(stringHTML)
        
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
        fileName['type'] = args[0][2][k]
        fileName['time'] = args[0][3][k]
        fileName['position'] = args[0][5][k]
        print args[0][1][k]
        k=k+1
        data.insert(0, fileName)
        pack.insert(0, data)
        i=i+1
        
        if any(inputt in l for l in listFile):
            continue;
        if(args[0][1][k-1] != 'url'):
            package = [inputt, mac]
            socketIO.emit('file', package)
            socketIO.wait(seconds=1)
        else:
            countFile = countFile-1
    ticker = {};
    ticker['message'] = args[0][4][0]
    ticker['behavior'] = args[0][4][1]
    playlist['assets'] = data
    playlist['ticker'] = ticker
    playlist['layout'] = args[0][6][0]
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

def receive_action(*args):
    #print args[0]
    try:
        json_data = open('/home/pi/media/control.json').read()
        control = json.loads(json_data)
    except:
        print "Main No Control"

    try:
        print control['control']['playlist']
        ticker = subprocess.Popen(["chromium-browser", "-kiosk","/home/pi/media/ticker/"+control['control']['playlist']+"_ticker.html"])
        #time.sleep(10)
    except:
        print "Main No ticker"
    if(args[0] == 'play'):
        #subprocess.Popen.kill(play)
        subprocess.call(["pkill", "-f", "mainPlay.py"])
        subprocess.call(["pkill", "-f", "toLeftSlide.py"])
        subprocess.call(["pkill", "-f", "leftSlide.py"])
        subprocess.call(["pkill", "-f", "mainImage.py"])
        subprocess.call(["killall", "omxplayer"])
        subprocess.call(["killall", "feh"])
        subprocess.call(["killall", "/usr/bin/omxplayer.bin"])
        time.sleep(1)
        global play
        play = subprocess.Popen(["python", "mainPlay.py"])
        leftSlide = subprocess.Popen(["python", 'toLeftSlide.py'], shell=False)
        time.sleep(1)
    #elif(args[0] == 'play'):

  
try:
    json_data = open('/home/pi/media/control.json').read()
    control = json.loads(json_data)
    print "read success"
except:
    print "Main No Control"

socketIO = SocketIO(server_ip, server_port, Namespace)

#time.sleep(5)
#subprocess.Popen.kill(play)
#subprocess.call(["killall", "/usr/bin/omxplayer.bin"])


ticker = subprocess.Popen(["chromium-browser", "-kiosk","/home/pi/media/ticker/"+control['control']['playlist']+"_ticker.html"])
#time.sleep(5)
play = subprocess.Popen(["python", "mainPlay.py"], shell=False)
leftSlide = subprocess.Popen(["python", 'toLeftSlide.py'], shell=False)
mac = getHwAddr('eth0')

while True:
    socketIO.on(mac+"_check", receive_check_file)
    socketIO.wait(seconds=1)
    socketIO.on(mac, receive_file)
    socketIO.wait(seconds=1)
    socketIO.on(mac+"_control", receive_control_file)
    socketIO.wait(seconds=1)
    socketIO.on('action', receive_action)
    socketIO.wait(seconds=1)
    socketIO.emit('mac', mac)
    socketIO.wait(seconds=1)
    time.sleep(10)
