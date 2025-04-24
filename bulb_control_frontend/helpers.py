"""Helpers file, has functions that are used by other files"""

__author__ = "Ryan Urquhart"
__contact__ = "https://github.com/RyanMcClean"

from socket import socket, AF_INET, SOCK_DGRAM, SO_BROADCAST, SOL_SOCKET, gaierror
import json


# This class is used to send and receive UDP packets to WizBulbs
class NetworkHandler:
    """NetworkHandler class, used to send and receive UDP packets to WizBulbs"""
    def __init__(self):
        # These are the packets defining specific functions for the bulbs
        self.bulb_packets = {
            "discover": b'{"method":"getPilot","params":{}}',
            "turn_on": b'{"id":1,"method":"setState","params":{"state":true}}',
            "turn_off": b'{"id":1,"method":"setState","params":{"state":false}}',
            "turn_to_half": b'{"id":1,"method":"setPilot","params":{"temp":2000,"dimming":10}}',
            "turn_to_full": b'{"id":1,"method":"setPilot","params":{"temp":2000,"dimming":100}}',
            # Registration is not currently used, but can be used in future development
            "registration": b'{"method":"registration","params":{"phoneMac":'
            b'"AAAAAAAAAAAA","register":false,"phoneIp":"1.2.3.4","id":"1"}}',
        }
        self.port = 38899
        self.client_sender = socket(AF_INET, SOCK_DGRAM)
        self.client_sender.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    # Used to send the packets to the bulbs, only sends UDP packets
    def sender(
        self,
        ip=None,
        packet="",
        timeout=2.5,
        attempts=3,
        color_params=None,
        expected_results=0,
    ) -> list:
        """Sends UDP packet to local ip address

        Args:
            ip (String): ip address to send the packet too.
            port (int): Port number to message on.
            packet (bytes): UDP packet to send.
            timeout (float, optional): Set timeout for listening for UDP response. Defaults to 0.5.
        """
        messages = []
        packet = self._match_packet(packet, color_params)
        self.client_sender.settimeout(timeout)
        try:
            continue_loop = True
            for _ in range(attempts):
                try:
                    self.client_sender.sendto(packet, (ip, self.port))
                    if expected_results < 0:
                        break

                    m, recv_ip = self.receive_message()
                    while m in list(self.bulb_packets.values()):
                        m, _ = self.receive_message()
                    while m is not None:
                        if (
                            "result" in m.keys()
                            and "success" in m["result"].keys()
                            and m["result"]["success"]
                        ):
                            continue_loop = False
                        message = m
                        message["ip"] = recv_ip
                        if message not in messages:
                            messages.append(message)
                        m, recv_ip = self.receive_message()
                except TimeoutError:
                    pass
                except gaierror as e:
                    print(e)
                    print(ip)
                if not continue_loop or (
                    expected_results == 0 or len(messages) >= expected_results
                ):
                    break
        except TimeoutError:
            print(f"Bulb query has timed out, {len(messages)} bulbs responded")
        except WindowsError:
            print("Unable to send UDP packet, please check your network connection - Windows Error")
        return messages

    # Listener for the UDP packets, used to receive messages from the bulbs
    def receive_message(self):
        """Listens for UDP packet returns from bulbs"""
        data, ip = self.client_sender.recvfrom(516)
        data = json.loads(data.decode("utf-8"))
        ip = ip[0]
        return data, ip

    # This matches the given string to the correct packet to send to the bulb
    def _match_packet(
        self,
        packet,
        color_params=None,
    ):
        match packet:
            case "discover":
                return self.bulb_packets["discover"]
            case "turn_on" | "turn_off":
                return self.bulb_packets[packet]
            case "turn_to_color":
                if color_params is None:
                    color_params = {"r": 0, "g": 0, "b": 0, "brightness": 0}
                return self.turn_to_color(
                    color_params["r"],
                    color_params["g"],
                    color_params["b"],
                    color_params["brightness"],
                )
            case "turn_to_full":
                return self.bulb_packets["turn_to_full"]
            case "turn_to_half":
                return self.bulb_packets["turn_to_half"]
            case _:
                raise ValueError("Input value for packet is not valid")

    # Helper to update bulb in the database
    def update_bulb_db(self, wiz_object) -> None:
        """Queries bulb to update the model in the db

        Args:
            wiz_object (WizBulb): WizBulb object to update
        """
        try:
            m = self.sender(wiz_object.bulb_ip, "discover")[0]
            m = m["result"] if "result" in m.keys() else {}
            wiz_object.bulb_state = m["state"] if "state" in m.keys() else False
            wiz_object.bulb_red = m["r"] if "r" in m.keys() else 0
            wiz_object.bulb_green = m["g"] if "g" in m.keys() else 0
            wiz_object.bulb_blue = m["b"] if "b" in m.keys() else 0
            wiz_object.bulb_temp = m["temp"] if "temp" in m.keys() else 0
            wiz_object.save()
        except IndexError:
            print("Unable to update bulb, using last known state")

    # turn_to_color is not used in the current implementation, but is left here for future development
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
            '{"id":1,"method":"setState","params":{"r": %d, "g": %d, "b": %d, "dimming": %d}}'
            % (r, g, b, brightness),
            encoding="utf-8",
        )
