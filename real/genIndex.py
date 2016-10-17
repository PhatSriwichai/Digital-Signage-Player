import os, subprocess, sys
import fcntl, struct, socket
import glob, json, time, codecs

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])
mac = getHwAddr('eth0')
ip = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]

stringHTML = "<!DOCTYPE html>"
stringHTML += "<html style=\"height:100%\">"
stringHTML += "<head></head>"
stringHTML += "<body style=\"height:100%; overflow:hidden; background-color:white;\">"
stringHTML += "<section style=\"height:15%\"></section>"
stringHTML += "<center><img src=\"/image/logo.png\"></center>"
stringHTML += "<center><h1>IP Address : "+ip+"</h1></center>"
stringHTML += "<center><h1>MAC Address : "+mac+"</h1></center></body></html>"
with codecs.open('/home/pi/Digital-Signage-Player/real/web/index.html', 'w', encoding='utf-8') as f:
    f.write(stringHTML)

index = subprocess.Popen(["chromium-browser", "-kiosk","web/index.html"])
