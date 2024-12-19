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
from . import variables

variables.init()


def index(request) -> HttpResponse:
    """Renders index, this changes depending on the type of request, and the contents of the request

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        HttpResponse: Page to render, index if the request is within expected boundaries
    """

    variables.separator()

    threading.Thread(target=variables.update_bulb_objects).start()

    variables.context["numBulbs"] = len(variables.context["bulbs"])
    if variables.context["numBulbs"] > 0:
        devices = getWorkingDeviceList()
        for device in devices:
            if device not in variables.context["audioDevices"]:
                variables.context["audioDevices"].append(device)
    variables.update_bulb_objects()

    if request.method == "POST":
        # Discover bulbs on network
        variables.messageLoud("form")
        if "bulbIp" in request.POST.keys():
            requestBody = request.POST
        else:
            requestBody = json.loads(request.body.decode("utf-8"))
        m = variables.client.sender(
            requestBody["bulbIp"],
            "discover",
            0.5,
            5,
        )
        if len(m) > 0:
            m = m[0]["result"] if "result" in m[0].keys() else m[0]
        elif len(m) == 1:
            m = m["result"] if "result" in m.keys() else m
        else:
            m = {}
        form = bulbForm(requestBody)
        if form.is_valid():
            model = form.save(commit=False)
            model.bulbState = m["state"] if "state" in m.keys() else False
            model.bulbRed = m["r"] if "r" in m.keys() else 0
            model.bulbGreen = m["g"] if "g" in m.keys() else 0
            model.bulbBlue = m["b"] if "b" in m.keys() else 0
            model.bulbTemp = m["temp"] if "temp" in m.keys() else 0
            model.save()
            bulbs = wizbulb.objects.all()
        else:
            variables.messageLoud("There is an error in the submitted form", "error")
            variables.context["error"] = True
            variables.context["errorMessage"] = "submitted bulb form was invalid"

        variables.separator()
        return render(request, "index.html", variables.context)

    elif request.method == "GET":
        variables.messageLoud("load home page")

        variables.context["error"] = False
        variables.context["errorMessage"] = ""

        variables.context["ips"] = list(set(variables.context["ips"]))
        variables.separator()
        return render(None, "index.html", variables.context)

    variables.separator()
    return redirect("404.html")


def discover(request) -> HttpResponse:
    variables.separator()
    threading.Thread(target=variables.update_bulb_objects).start()

    ip = "255.255.255.255"
    variables.messageLoud("discover")
    m = variables.client.sender(ip, packet="discover", attempts=5, expected_results=100)

    for bulbResponse in m:
        if [True for bulb in variables.context["bulbs"] if bulbResponse["ip"] in bulb["BulbIp"]]:
            variables.messageLoud("Hiding already saved bulb")
        elif bulbResponse["ip"] not in variables.context["ips"]:
            variables.context["ips"].append(bulbResponse["ip"])

    if (
        not variables.context["numBulbs"] > 0
        and not len(variables.context["ips"]) > 0
        and len(variables.context["bulbs"]) < 0
    ):
        variables.context["error"] = True
        variables.context["errorMessage"] = (
            "Bulb discovery failed. Please ensure bulbs are connected to the same network as your computer."
        )
        variables.messageLoud(
            "Bulb discovery failed. Please ensure bulbs are connected to the same network as your computer."
        )

    variables.separator()
    return render(request, "index.html", variables.context)


def toggle_bulb(request) -> JsonResponse:
    """Toggles WizLight bulb

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        JsonResponse: State of bulb after toggle
        HttpResponse: 404 page if there is an error
    """
    variables.separator()

    if request.method == "POST":
        # Flicker specific bulb
        if "ip" in request.POST.keys() or "ip" in request.body.decode("utf-8"):
            ip = request.POST["ip"] if "ip" in request.POST.keys() else json.loads(request.body.decode("utf-8"))["ip"]
            variables.messageLoud(f"Toggling bulb at: {ip}")
            m = variables.client.sender(ip, "discover", 0.5, 5)
            if len(m) > 0 and "result" in m[0].keys():
                m = m[0]["result"]
                if m["state"]:
                    variables.client.sender(ip, "turn_off")
                else:
                    variables.client.sender(ip, "turn_on")

                m = variables.client.sender(ip, "discover", 0.5)
                m = m["result"] if "result" in m.keys() else m
            else:
                m = {"error": "could not query bulb"}
                variables.messageLoud("Could not query bulb", "error")
            variables.separator()
            return JsonResponse(m)

    variables.separator()
    return render(request, "404.html", status=404)


def query_bulb(request) -> JsonResponse | HttpResponse:
    """Query bulb for its current state

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        JsonResponse: Returns state of bulb
        HttpResponse: Renders 404 page
    """
    variables.separator()
    variables.messageLoud("query bulb")

    if request.method == "POST":
        request = request.POST if request.body is None else json.loads(request.body.decode("utf-8"))
        ip = request["ip"]
        m = variables.client.sender(ip, "discover", expected_results=1, attempts=1)
        if len(m) > 0 and "result" in m[0].keys():
            m = m[0]["result"]
            if "state" in m.keys():
                variables.separator()
                return JsonResponse(m)
    variables.messageLoud("Query error", "error")
    variables.separator()
    return JsonResponse({"error": "could not query bulb"})


def color_bulb(request) -> JsonResponse | HttpResponse:
    """Change the bulb to a given colour, represented by rgb values

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        JsonResponse: Returns result of bulb color change
        HttpResponse: If error render 404 not found page
    """
    variables.separator()
    threading.Thread(target=variables.update_bulb_objects).start()
    variables.messageLoud("color bulb")

    if request.method == "POST":
        if "ip" in request.POST.keys() or "ip" in json.loads(request.body).keys():
            body = request.POST if "ip" in request.POST.keys() else json.loads(request.body)
            ip = body["ip"]

            m = variables.client.sender(
                ip,
                packet="turn_to_color",
                color_params={"r": int(body["r"]), "g": int(body["g"]), "b": int(body["b"]), "brightness": 255},
            )
            if len(m) > 0:
                m = m[0]["result"]

                variables.messageLoud(f"{ip} - {m}")

                variables.separator()
                return JsonResponse(m)
    variables.messageLoud("Error, could not query bulb", "error")
    variables.separator()
    return JsonResponse({"error": "could not query bulb"})


def activate_music_sync(request) -> JsonResponse:
    """This will 'eventually' activate the music sync function of the application, WIP

    Args:
        request HttpRequest: HttpRequest object supplied by Django
    """
    variables.separator()
    variables.messageLoud("Starting Audio Sync")

    if request.body.decode("utf-8").isdigit():
        variables.messageLoud(int(request.body.decode("utf-8")))
        x = threading.Thread(
            target=audioSync,
            args=(
                variables.client,
                int(request.body.decode("utf-8")),
            ),
        )
        # x.start()

        sleep(5)
        if x.is_alive:
            variables.separator()
            return JsonResponse({"result": True})

    variables.messageLoud("Audio Sync did not stop", "error")
    variables.separator()
    return JsonResponse({"result": False})


def stop_audio_sync(request) -> None:
    variables.separator()
    variables.messageLoud("Stopping Audio Sync")
