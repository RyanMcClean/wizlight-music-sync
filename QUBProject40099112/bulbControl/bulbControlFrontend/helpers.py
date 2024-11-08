from socket import *
from time import sleep
import json

# Sends UDP packet to specific IP, listens for response
def sendUDPPacket(ip, port, packet, timeout=0.5):
    while True:
        try:
            sock = socket(AF_INET, SOCK_DGRAM)
            sock.bind(('', port))
            sock.settimeout(timeout)
            sock.sendto(packet, (ip, port))
            m = sock.recvfrom(516)
            sock.close()
            return m
        except:
            sleep(0.1)

def updateBulbObjects(wizObj):
    from .views import discover, port
    m = json.loads(sendUDPPacket(wizObj.bulbIp, port, discover)[0].decode("utf-8"))
    m = m['result'] if 'result' in m.keys() else ''
    wizObj.bulbState = m['state']
    wizObj.bulbRed = m['r'] if 'r' in m.keys() else 0
    wizObj.bulbGreen = m['g'] if 'g' in m.keys() else 0
    wizObj.bulbBlue = m['b'] if 'b' in m.keys() else 0
    wizObj.bulbTemp = m['temp'] if 'temp' in m.keys() else 0
    wizObj.save()
    print(wizObj)
    pass
