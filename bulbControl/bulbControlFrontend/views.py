"""Views file for Django module.
Defines a series of views and actions to be taken on requests to the API
"""

__author__ = "Ryan McClean"
__contact__ = "https://github.com/RyanMcClean"


from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, timeout
from time import sleep, time_ns
import json
import os
import threading

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from .forms import bulbForm
from .models import wizbulb
from .audioTesting import main as audioSync, getWorkingDeviceList

discover = b'{"method":"getPilot","params":{}}'
turn_on = b'{"id":1,"method":"setState","params":{"state":true}}'
turn_off = b'{"id":1,"method":"setState","params":{"state":false}}'
port = 38899

from .helpers import update_bulb_objects, send_udp_packet, turn_to_color  # noqa: E402


def index(request) -> HttpResponse:
    """Renders index, this changes depending on the type of request, and the contents of the request

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        HttpResponse: Page to render, index if the request is within expected boundaries
    """

    # To add a limit to the returned bulb objects the line would read:
    # bulbs = wizbulb.objects.all()[x]
    # where x is the number of bulb objects returned
    bulbs = wizbulb.objects.all()

    context = {"regForm": bulbForm(), "ips": [], "count": 0, "bulbs": [], "numBulbs": 0, "audioDevices": []}
    for x in bulbs:
        update_bulb_objects(x)
        context["bulbs"].append(x.returnJSON())

    context["numBulbs"] = len(context["bulbs"])
    if context["numBulbs"] > 0:
        devices = getWorkingDeviceList()
        for device in devices:
            context["audioDevices"].append(device)
    print("-" * os.get_terminal_size()[0])

    if request.method == "POST":
        # Discover bulbs on network
        if "discover" in request.POST.keys():
            print("discover")
            sock = socket(AF_INET, SOCK_DGRAM)
            sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
            sock.bind(("", port))
            sock.settimeout(0.5)
            sock.sendto(discover, ("255.255.255.255", port))
            m = sock.recvfrom(516)
            count = 0
            while m != None:
                if m[0] != discover:
                    bulbResponse = json.loads(m[0].decode("utf-8"))

                    if [
                        True
                        for bulb in context["bulbs"]
                        if str(m[1]).replace("(", "").replace("'", "").split(",", maxsplit=1)[0] in bulb["BulbIp"]
                    ]:
                        print("Hiding already saved bulb")
                    else:
                        context["count"] = range(count)
                        context["ips"].append(str(m[1]).replace("(", "").replace("'", "").split(",", maxsplit=1)[0])
                        count += 1
                try:
                    m = sock.recvfrom(516)
                except timeout:
                    m = None

            print("-" * os.get_terminal_size()[0])
            sock.close()

            return render(request, "index.html", context)

            # Create bulb object in db
        else:
            print("form")
            m = send_udp_packet(request.POST["bulbIp"], port, discover)
            bulbResponse = json.loads(m[0].decode("utf-8"))["result"]
            form = bulbForm(request.POST)
            print("Form: ")
            print(form)
            if form.is_valid():
                model = form.save(commit=False)
                model.bulbState = bulbResponse["state"]
                model.bulbRed = bulbResponse["r"] if "r" in bulbResponse.keys() else 0
                model.bulbGreen = bulbResponse["g"] if "g" in bulbResponse.keys() else 0
                model.bulbBlue = bulbResponse["b"] if "b" in bulbResponse.keys() else 0
                model.bulbTemp = bulbResponse["temp"] if "temp" in bulbResponse.keys() else 0
                model.save()
                bulbs = wizbulb.objects.all()
                return render(request, "index.html", context)
            else:
                pass

            return render(request, "index.html", context)

    elif request.method == "GET":
        print(request.GET)
        print("load home page")
        print("-" * os.get_terminal_size()[0])

        return render(None, "index.html", context)

    return redirect("404.html")


def toggle_bulb(request) -> JsonResponse | HttpResponse:
    """Toggles WizLight bulb

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        JsonResponse: State of bulb after toggle
        HttpResponse: 404 page if there is an error
    """

    if request.method == "POST":
        print(request.POST)

        # Flicker specific bulb
        if "ip" in request.POST.keys() or "ip" in json.loads(request.body.decode("utf-8")).keys():
            print("toggle")
            ip = request.POST["ip"] if "ip" in request.POST.keys() else json.loads(request.body.decode("utf-8"))["ip"]
            print("-" * os.get_terminal_size()[0])
            startTime = time_ns()
            m = json.loads(send_udp_packet(ip, port, discover)[0].decode("utf-8"))["result"]
            endTime = time_ns()
            totalTime = (endTime - startTime) / 1000000000
            print("Toggle time: " + str(totalTime))
            if m["state"]:
                send_udp_packet(ip, port, turn_off)
                m = json.loads(send_udp_packet(ip, port, discover)[0].decode("utf-8"))["result"]
                return JsonResponse(m)
            else:
                send_udp_packet(ip, port, turn_on)
                m = json.loads(send_udp_packet(ip, port, discover)[0].decode("utf-8"))["result"]
                return JsonResponse(m)
        return redirect("404.html")


def query_bulb(request) -> JsonResponse | HttpResponse:
    """Query bulb for its current state

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        JsonResponse: Returns state of bulb
        HttpResponse: Renders 404 page
    """
    if request.method == "POST":
        print(request.POST)
        body = json.loads(request.body.decode("utf-8")) if request.body else None
        # Flicker specific bulb
        if "ip" in request.POST.keys() or "ip" in body.keys():
            print("query bulb")
            ip = request.POST["ip"] if "ip" in request.POST.keys() else body["ip"]
            print("-" * os.get_terminal_size()[0])

            m = json.loads(send_udp_packet(ip, port, discover)[0].decode("utf-8"))["result"]
            if m["state"]:
                return JsonResponse(m)
            else:
                return JsonResponse(m)
    return redirect("404.html")


def color_bulb(request) -> JsonResponse | HttpResponse:
    """Change the bulb to a given colour, represented by rgb values

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        JsonResponse: Returns result of bulb color change
        HttpResponse: If error render 404 not found page
    """
    if request.method == "POST":
        print(request.POST)
        body = json.loads(request.body.decode("utf-8")) if request.body else None
        if "ip" in request.POST.keys() or "ip" in body.keys():
            print("color bulb")
            ip = "192.168.50.128"
            print("-" * os.get_terminal_size()[0])

            m = json.loads(
                send_udp_packet(ip, port, turn_to_color(r=body["r"], g=body["g"], b=body["b"], brightness=255))[
                    0
                ].decode("utf-8")
            )["result"]
            print(m)
            m = (
                json.loads(send_udp_packet(ip, port, discover)[0].decode("utf-8"))["result"]
                if m["success"]
                else json.loads({"result": False})
            )
            return JsonResponse(m)
    return redirect("404.html")


def activate_music_sync(request) -> None:
    """This will 'eventually' activate the music sync function of the application, WIP

    Args:
        request HttpRequest: HttpRequest object supplied by Django
    """
    print(request.POST)
    print("-" * os.get_terminal_size()[0])
    if "audio_device" in request.POST.keys():
        print(int(request.POST["audio_device"]))
        sleep(10)
        x = threading.Thread(target=audioSync, args=(int(request.POST["audio_device"])))
        x.start()
        return JsonResponse({"result": "audio sync started"})

    return redirect("404.html")
