"""Helpers file, has functions that are used by other files"""

__author__ = "Ryan McClean"
__contact__ = "https://github.com/RyanMcClean"

from socket import socket, AF_INET, SOCK_DGRAM, SO_BROADCAST, SOL_SOCKET, gaierror
import json
import os


class NetworkHandler:
    def __init__(self):
        self.bulbPackets = {
            "discover": b'{"method":"getPilot","params":{}}',
            "turn_on": b'{"id":1,"method":"setState","params":{"state":true}}',
            "turn_off": b'{"id":1,"method":"setState","params":{"state":false}}',
            "turn_to_half": b'{"id":1,"method":"setPilot","params":{"temp":2000,"dimming":10}}',
            "turn_to_full": b'{"id":1,"method":"setPilot","params":{"temp":2000,"dimming":100}}',
            "registration": b'{"method":"registration","params":{"phoneMac":"AAAAAAAAAAAA","register":false,"phoneIp":"1.2.3.4","id":"1"}}',
        }
        self.port = 38899
        self.clientSender = socket(AF_INET, SOCK_DGRAM)
        self.clientSender.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    def sender(self, ip=None, packet="", timeout=2.5, attempts=3, color_params={}, expected_results=1) -> list:
        """Sends UDP packet to local ip address

        Args:
            ip (String): ip address to send the packet too.
            port (int): Port number to message on.
            packet (bytes): UDP packet to send.
            timeout (float, optional): Set timeout for listening for UDP response. Defaults to 0.5.
        """
        messages = []
        packet = self._match_packet(packet, color_params)
        self.clientSender.settimeout(timeout)
        try:
            continue_loop = True
            for x in range(attempts):
                try:
                    self.clientSender.sendto(packet, (ip, self.port))

                    m, recv_ip = self.receive_message()
                    while m in list(self.bulbPackets.values()):
                        m, revc_ip = self.receive_message()
                    while m is not None:
                        if "result" in m.keys() and "success" in m["result"].keys() and m["result"]["success"]:
                            continue_loop = False
                        message = m
                        message["ip"] = recv_ip
                        if message not in messages:
                            messages.append(message)
                        m, rev_ip = self.receive_message()
                except TimeoutError:
                    pass
                except gaierror as e:
                    print(e)
                    print(ip)
                if not continue_loop or len(messages) >= expected_results:
                    break
        except TimeoutError:
            print(f"Bulb query has timed out, {len(messages)} bulbs responded")
        except Exception as e:
            print("General exception")
            import traceback

            traceback.print_exc()
            print(e)
        return messages

    def receive_message(self):
        data, ip = self.clientSender.recvfrom(516)
        data = json.loads(data.decode("utf-8"))
        ip = ip[0]
        return data, ip

    def _match_packet(
        self,
        packet,
        color_params={"r": 0, "g": 0, "b": 0, "brightness": 0},
    ):
        match packet:
            case "discover":
                return self.bulbPackets["discover"]
            case "turn_on" | "turn_off":
                return self.bulbPackets[packet]
            case "turn_to_color":
                return self.turn_to_color(
                    color_params["r"], color_params["g"], color_params["b"], color_params["brightness"]
                )
            case "turn_to_full":
                return self.bulbPackets["turn_to_full"]
            case "turn_to_half":
                return self.bulbPackets["turn_to_half"]
            case _:
                raise ValueError("Input value for packet is not valid")

    def update_bulb_objects(self, wizObj) -> None:
        """Queries bulb to update the model in the db

        Args:
            wizObj (WizBulb): WizBulb object to update
        """
        try:
            m = self.sender(wizObj.bulbIp, "discover")[0]
            m = m["result"] if "result" in m.keys() else {}
            wizObj.bulbState = m["state"] if "state" in m.keys() else False
            wizObj.bulbRed = m["r"] if "r" in m.keys() else 0
            wizObj.bulbGreen = m["g"] if "g" in m.keys() else 0
            wizObj.bulbBlue = m["b"] if "b" in m.keys() else 0
            wizObj.bulbTemp = m["temp"] if "temp" in m.keys() else 0
            wizObj.save()
        except IndexError:
            print("Unable to update bulb, using last known state")

    def turn_to_color(self, r=0, g=0, b=0, brightness=0) -> bytes:
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
