import json
from pprint import pprint

#with open('/home/pi/Digital-Signage-Player/test/playlist.json') as data_file:    
#    data = json.load(data_file)
data = json.load(open("/home/pi/Digital-Signage-Player/test/playlist.json").read())
pprint(data)
