import fcntl, socket, struct
from socketIO_client import SocketIO, BaseNamespace
import time
server_ip = '192.168.137.2'

class Namespace(BaseNamespace):

    def on_aaa_response(self, *args):
        print('on_aaa_response', args)
        self.emit('bbb')

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])

mac = getHwAddr('eth0')

socketIO = SocketIO(server_ip, 8080, Namespace)


while True:
    socketIO.emit('mac', mac)
    socketIO.wait(seconds=1)
    time.sleep(10)

