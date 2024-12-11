"""Helpers file, has functions that are used by other files"""

__author__ = "Ryan McClean"
__contact__ = "https://github.com/RyanMcClean"

from socket import socket, AF_INET, SOCK_DGRAM, SO_BROADCAST, SOL_SOCKET, IPPROTO_UDP
import json
import os

bulbPackets = {
    "discover": b'{"method":"getPilot","params":{}}',
    "turn_on": b'{"id":1,"method":"setState","params":{"state":true}}',
    "turn_off": b'{"id":1,"method":"setState","params":{"state":false}}',
}
port = 38899


def send_udp_packet(
    ip=None, port=38899, packet="", timeout=1.0, attempts=1, color_params={"r": 0, "g": 0, "b": 0, "brightness": 0}
) -> dict | None:
    """Sends UDP packet to local ip address

    Args:
        ip (String): ip address to send the packet too.
        port (int): Port number to message on.
        packet (bytes): UDP packet to send.
        timeout (float, optional): Set timeout for listening for UDP response. Defaults to 0.5.
    """
    messages = []
    try:
        sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        match packet:
            case "discover":
                packet = bulbPackets["discover"]
                sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
                # sock.bind(("", port))
            case "query":
                packet = bulbPackets["discover"]
                # sock.bind((ip, port))
            case "turn_on" | "turn_off":
                packet = bulbPackets[packet]
                # sock.bind((ip, port))
            case "turn_to_color":
                packet = turn_to_color(
                    color_params["r"], color_params["g"], color_params["b"], color_params["brightness"]
                )
                # sock.bind((ip, port))
            case _:
                raise ValueError("Input value for packet is not valid")

        sock.bind(("", port))
        sock.settimeout(timeout)
        for x in range(attempts):
            try:
                sock.sendto(packet, (ip, port))
                m = sock.recvfrom(516)
                while packet in m:
                    m = sock.recvfrom(516)
                while m is not None:
                    message = json.loads((m[0].decode("utf-8")))
                    message["ip"] = m[1][0]
                    messages.append(message)
                    m = sock.recvfrom(516)
            except TimeoutError:
                pass
    except TimeoutError:
        print(f"Bulb query has timed out, {len(messages)} bulbs responded")
    except Exception as e:
        print("General exception")
        import traceback

        traceback.print_exc()
        print(e)
    finally:
        sock.close()
    return messages


def update_bulb_objects(wizObj) -> None:
    """Queries bulb to update the model in the db

    Args:
        wizObj (WizBulb): WizBulb object to update
    """

    m = send_udp_packet(wizObj.bulbIp, packet="discover")[0]
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
