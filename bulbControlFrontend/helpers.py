"""Helpers file, has functions that are used by other files"""

__author__ = "Ryan McClean"
__contact__ = "https://github.com/RyanMcClean"

from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep
import json, os


def send_udp_packet(ip, port, packet, timeout=10.0) -> dict | None:
    """Sends UDP packet to local ip address

    Args:
        ip (String): ip address to send the packet too.
        port (int): Port number to message on.
        packet (bytes): UDP packet to send.
        timeout (float, optional): Set timeout for listening for UDP response. Defaults to 0.5.
    """
    while True:
        try:
            sock = socket(AF_INET, SOCK_DGRAM)
            sock.bind((ip, port))
            sock.settimeout(timeout)
            sock.sendto(packet, (ip, port))
            m = sock.recvfrom(516)
            sock.close()
            if m is not None:
                message = json.loads((m[0].decode("utf-8")))
                message["ip"] = m[1][0]
            else:
                message = {"error": "no response"}
            return message
        except TimeoutError:
            return None


def update_bulb_objects(wizObj) -> None:
    """Queries bulb to update the model in the db

    Args:
        wizObj (WizBulb): WizBulb object to update
    """
    from .views import port, discover

    m = json.loads(send_udp_packet(wizObj.bulbIp, port, discover)[0].decode("utf-8"))
    m = m["result"] if "result" in m.keys() else ""
    wizObj.bulbState = m["state"]
    wizObj.bulbRed = m["r"] if "r" in m.keys() else 0
    wizObj.bulbGreen = m["g"] if "g" in m.keys() else 0
    wizObj.bulbBlue = m["b"] if "b" in m.keys() else 0
    wizObj.bulbTemp = m["temp"] if "temp" in m.keys() else 0
    wizObj.save()


def turn_to_color(r=0, g=0, b=0, brightness=0) -> bytes:
    """Returns bytes packet to turn Wizbulb to specific colour

    Args:
        r (int, optional): Red value. Defaults to 0.
        g (int, optional): Green value. Defaults to 0.
        b (int, optional): Blue value. Defaults to 0.
        brightness (int, optional): _description_. Defaults to 0.

    Returns:
        bytes: _description_
    """
    return bytes(
        '{"id":1,"method":"setState","params":{"r": %d, "g": %d, "b": %d, "dimming": %d}}' % (r, g, b, brightness),
        encoding="utf-8",
    )


def separator() -> None:
    try:
        print("-" * os.get_terminal_size()[0])
    except OSError:
        print("-" * 5)
