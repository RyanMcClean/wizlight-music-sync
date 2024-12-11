"""Views file for Django module.
Defines a series of views and actions to be taken on requests to the API
"""

__author__ = "Ryan McClean"
__contact__ = "https://github.com/RyanMcClean"

from time import sleep
import json
import threading

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from .forms import bulbForm
from .models import wizbulb
from .audioTesting import main as audioSync, getWorkingDeviceList


from .helpers import update_bulb_objects, send_udp_packet, separator  # noqa: E402


def index(request) -> HttpResponse:
    """Renders index, this changes depending on the type of request, and the contents of the request

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        HttpResponse: Page to render, index if the request is within expected boundaries
    """

    separator()
    # To add a limit to the returned bulb objects the line would read:
    # bulbs = wizbulb.objects.all()[x]
    # where x is the number of bulb objects returned
    bulbs = wizbulb.objects.all()

    context = {
        "regForm": bulbForm(),
        "ips": [],
        "count": 0,
        "bulbs": [],
        "numBulbs": 0,
        "audioDevices": [],
        "error": False,
        "errorMessage": "",
    }
    for x in bulbs:
        update_bulb_objects(x)
        context["bulbs"].append(x.returnJSON())

    context["numBulbs"] = len(context["bulbs"])
    if context["numBulbs"] > 0:
        devices = getWorkingDeviceList()
        for device in devices:
            context["audioDevices"].append(device)

    if request.method == "POST":
        # Discover bulbs on network
        if "discover" in request.POST.keys() or "discover" in request.body.decode("utf-8"):
            if "discover" in request.POST.keys():
                ip = "255.255.255.255" if len(request.POST["discover"]) == 0 else request.POST["discover"]
            else:
                ip = (
                    "255.255.255.255"
                    if len(json.loads(request.body.decode("utf-8"))["discover"]) == 0
                    else json.loads(request.body.decode("utf-8"))["discover"]
                )
            print("discover")
            m = send_udp_packet(ip, packet="discover", attempts=5)
            context["count"] = len(m)

            for bulbResponse in m:
                print(bulbResponse)
                if [
                    True
                    for bulb in context["bulbs"]
                    if str(m[1]).replace("(", "").replace("'", "").split(",", maxsplit=1)[0] in bulb["BulbIp"]
                ]:
                    print("Hiding already saved bulb")
                else:
                    context["ips"].append(bulbResponse["ip"])

            if not context["numBulbs"] > 0 and not len(context["ips"]) > 0:
                context["error"] = True
                context["errorMessage"] = (
                    "Bulb discovery failed. Please ensure bulbs are connected to the same network as your computer."
                )
                print("Bulb discovery failed. Please ensure bulbs are connected to the same network as your computer.")

            separator()
            return render(request, "index.html", context)

            # Create bulb object in db
        else:
            print("form")
            if "bulbIp" in request.POST.keys():
                requestBody = request.POST
            else:
                requestBody = json.loads(request.body.decode("utf-8"))
            m = send_udp_packet(
                requestBody["bulbIp"],
                "discover",
                0.5,
                5,
            )
            if len(m) > 1:
                m = m[0]["result"] if "result" in m[0].keys() else m[0]
            elif len(m) == 1:
                m = m["result"] if "result" in m.keys() else m
            else:
                m = {}
            form = bulbForm(requestBody)
            print("Form: ")
            print(form)
            if form.is_valid():
                model = form.save(commit=False)
                model.bulbState = m["state"] if "state" in m.keys() else False
                model.bulbRed = m["r"] if "r" in m.keys() else 0
                model.bulbGreen = m["g"] if "g" in m.keys() else 0
                model.bulbBlue = m["b"] if "b" in m.keys() else 0
                model.bulbTemp = m["temp"] if "temp" in m.keys() else 0
                model.save()
                bulbs = wizbulb.objects.all()
                separator()
                return render(request, "index.html", context)
            else:
                context["error"] = True
                context["errorMessage"] = "submitted bulb form was invalid"

            separator()
            return render(request, "index.html", context)

    elif request.method == "GET":
        print(request.GET)
        print("load home page")

        separator()
        return render(None, "index.html", context)

    separator()
    return redirect("404.html")


def toggle_bulb(request) -> JsonResponse:
    """Toggles WizLight bulb

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        JsonResponse: State of bulb after toggle
        HttpResponse: 404 page if there is an error
    """
    separator()
    print(request)
    if request.method == "POST":
        print(request)

        # Flicker specific bulb
        if "ip" in request.POST.keys() or "ip" in request.body.decode("utf-8"):
            print("toggle")
            ip = request.POST["ip"] if "ip" in request.POST.keys() else json.loads(request.body.decode("utf-8"))["ip"]
            m = send_udp_packet(ip, "query", 0.5, 5)
            if len(m) > 0 and "result" in m[0].keys():
                m = m["result"]
                if m["state"]:
                    send_udp_packet(ip, "turn_off")
                else:
                    send_udp_packet(ip, "turn_on")

                m = send_udp_packet(ip, "query", 0.5)
                m = m["result"] if "result" in m.keys() else m
            else:
                m = {"error": "could not query bulb"}
            separator()
            return JsonResponse(m)

    separator()
    return render(request, "404.html", status=404)


def query_bulb(request) -> JsonResponse | HttpResponse:
    """Query bulb for its current state

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        JsonResponse: Returns state of bulb
        HttpResponse: Renders 404 page
    """
    separator()
    print("query bulb")

    if request.method == "POST":
        print("Request - " + str(request.POST) if request.body is None else "Request - " + request.body.decode("utf-8"))
        request = request.POST if request.body is None else json.loads(request.body.decode("utf-8"))
        ip = request["ip"]
        m = send_udp_packet(ip, packet="query", timeout=0.25)
        if len(m) > 0 and "result" in m[0].keys():
            m = m[0]["result"]
            print("Bulb Response - " + str(m))
            if "state" in m.keys():
                separator()
                return JsonResponse(m)
    separator()
    return JsonResponse({"error": "could not query bulb"})


def color_bulb(request) -> JsonResponse | HttpResponse:
    """Change the bulb to a given colour, represented by rgb values

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        JsonResponse: Returns result of bulb color change
        HttpResponse: If error render 404 not found page
    """
    separator()
    if request.method == "POST":
        print(request)
        if "ip" in request.POST.keys() or "ip" in json.loads(request.body).keys():
            body = request.POST if "ip" in request.POST.keys() else json.loads(request.body)
            print("color bulb")
            ip = body["ip"]

            m = send_udp_packet(
                ip,
                packet="turn_to_color",
                color_params={"r": int(body["r"]), "g": int(body["g"]), "b": int(body["b"]), "brightness": 255},
                timeout=0.5,
            )
            print(m)
            if len(m) > 0:
                m = m[0]["result"]
                print(m)
                m = send_udp_packet(ip, packet="query")
                if len(m) > 0:
                    m = m[0]["result"]
                    separator()
                    return JsonResponse(m)
    separator()
    return JsonResponse({"error": "could not query bulb"})


def activate_music_sync(request) -> None:
    """This will 'eventually' activate the music sync function of the application, WIP

    Args:
        request HttpRequest: HttpRequest object supplied by Django
    """
    separator()
    print(request.POST)

    if "audio_device" in request.POST.keys():
        print(int(request.POST["audio_device"]))
        sleep(10)
        x = threading.Thread(target=audioSync, args=(int(request.POST["audio_device"])))
        x.start()
        separator()
        return JsonResponse({"result": "audio sync started"})

    separator()
    return redirect("404.html")
