# pylint: disable=E1101, unnecessary-pass
"""Views file for Django module.
Defines a series of views and actions to be taken on requests to the API
"""

__author__ = "Ryan Urquhart"
__contact__ = "https://github.com/RyanMcClean"

from time import sleep
import json
import threading

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from bulb_control_frontend import models

from .forms import BulbForm
from .models import Wizbulb
from .audio_handler import main as audioSync
from . import variables


if not variables.READY:
    variables.init()


def index(request) -> HttpResponse:
    """Renders index, this changes depending on the type of request, and the contents of the request

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        HttpResponse: Page to render, index if the request is within expected boundaries
    """

    variables.separator()

    variables.context["numBulbs"] = len(variables.context["bulbs"])

    if request.method == "POST":
        # save new bulb
        variables.message_loud("form")
        if "bulb_ip" in request.POST.keys():
            request_body = request.POST
        else:
            request_body = json.loads(request.body.decode("utf-8"))
        m = variables.client.sender(
            request_body["bulb_ip"],
            "discover",
            0.5,
            5,
        )
        if len(m) > 0:
            m = m[0]["result"] if "result" in m[0].keys() else m[0]
        else:
            m = {}
        form = BulbForm(request_body)
        if form.is_valid():
            model = form.save(commit=False)
            model.bulb_state = m["state"] if "state" in m.keys() else False
            model.bulb_red = m["r"] if "r" in m.keys() else 0
            model.bulb_green = m["g"] if "g" in m.keys() else 0
            model.bulb_blue = m["b"] if "b" in m.keys() else 0
            model.bulb_temp = m["temp"] if "temp" in m.keys() else 0
            model.save()
            variables.context["bulbs"].append(model.return_json())
            variables.context["numBulbs"] = len(variables.context["bulbs"])
            variables.context["ips"].remove(model.bulb_ip)
            variables.context["success"] = True
            variables.context["successMessage"] = f"Bulb {model.bulb_name} added successfully"
        else:
            variables.message_loud("There is an error in the submitted form", "error")
            variables.context["error"] = True
            variables.context["errorMessage"] = "submitted bulb form was invalid"

        variables.update_bulb_objects()
        variables.separator()
        return render(request, "index.html", variables.context)

    if request.method == "GET":
        variables.message_loud("load home page")

        variables.separator()
        return render(request, "index.html", variables.context)

    variables.separator()
    return render(request, "404.html", status=404)


def discover(request) -> HttpResponse:
    """Renders index, before rendering index it does a search for bulbs on the local network,
        this changes depending on the type of request, and the contents of the request

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        HttpResponse: Page to render, index if the request is within expected boundaries
    """
    variables.separator()

    audio_thread = threading.Thread(target=variables.update_working_audio_devices)
    audio_thread.start()

    if request.method == "GET":
        ip = "255.255.255.255"
        variables.message_loud("discover")
        m = variables.client.sender(ip, packet="discover", attempts=5)
        variables.context["ips"] = []
        for bulb_response in m:
            if [
                True
                for bulb in variables.context["bulbs"]
                if bulb_response["ip"] in bulb["bulb_ip"]
            ]:
                variables.message_loud("Hiding already saved bulb")
            elif bulb_response["ip"] not in variables.context["ips"]:
                variables.context["ips"].append(bulb_response["ip"])

        if (
            variables.context["numBulbs"] <= 0
            and len(variables.context["ips"]) <= 0
            and len(variables.context["bulbs"]) <= 0
        ):
            variables.context["error"] = True
            variables.context["errorMessage"] = (
                "Bulb discovery failed. Please ensure bulbs are "
                + "connected to the same network as your computer."
            )
            variables.message_loud(
                "Bulb discovery failed. Please ensure bulbs are "
                + "connected to the same network as your computer."
            )
        else:
            variables.context["ips"] = list(set(variables.context["ips"]))
        variables.separator()
        return render(request, "index.html", variables.context)

    variables.separator()
    return render(request, "404.html", status=404)


def toggle_bulb(request) -> JsonResponse | HttpResponse:
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
            ip = (
                request.POST["ip"]
                if "ip" in request.POST.keys()
                else json.loads(request.body.decode("utf-8"))["ip"]
            )
            variables.message_loud(f"Toggling bulb at: {ip}")
            m = variables.client.sender(ip, "discover", 0.5, 5)
            if len(m) > 0 and "result" in m[0].keys():
                m = m[0]["result"]
                if m["state"]:
                    variables.client.sender(ip, "turn_off")
                else:
                    variables.client.sender(ip, "turn_on")

                m = variables.client.sender(ip, "discover", expected_results=1)
                m = m[0]["result"] if len(m) > 0 and "result" in m[0].keys() else m
            else:
                m = {"error": "could not query bulb"}
                variables.message_loud("Could not query bulb", "error")
            variables.separator()
            return JsonResponse(m)

    variables.separator()
    return render(request, "404.html", status=404)


def query_bulb(request) -> JsonResponse | HttpResponse:
    """Query bulb for its current state, updates object in database

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        JsonResponse: Returns state of bulb
        HttpResponse: Renders 404 page
    """
    variables.separator()
    variables.message_loud("query bulb")

    if request.method == "POST":
        request = request.POST if request.body is None else json.loads(request.body.decode("utf-8"))
        ip = request["ip"] if "ip" in request.keys() else None
        if ip:
            try:
                bulb = Wizbulb.objects.get(bulb_ip=ip)
                m = variables.client.sender(ip, "discover", expected_results=1, attempts=1)
                if len(m) > 0 and "result" in m[0].keys():
                    m = m[0]
                    if "state" in m["result"].keys():
                        bulb.bulb_state = m["result"]["state"]
                        bulb.bulb_red = m["result"]["r"] if "r" in m["result"].keys() else 0
                        bulb.bulb_green = m["result"]["g"] if "g" in m["result"].keys() else 0
                        bulb.bulb_blue = m["result"]["b"] if "b" in m["result"].keys() else 0
                        bulb.bulb_temp = m["result"]["temp"]
                        bulb.bulb_brightness = m["result"]["dimming"]
                        bulb.save()
                        variables.separator()
                        return JsonResponse(m)
            except models.Wizbulb.DoesNotExist:
                variables.message_loud(f"Bulb at {ip} does not exist", "error")
                variables.separator()
                return JsonResponse({"error": "bulb does not exist"})

            variables.message_loud("Query error", "error")
            variables.separator()
            return JsonResponse({"error": "could not query bulb"})

    variables.separator()
    return render(request, "404.html", status=404)


def color_bulb(request) -> JsonResponse | HttpResponse:
    """Change the bulb to a given colour, represented by rgb values

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        JsonResponse: Returns result of bulb color change
        HttpResponse: If error render 404 not found page
    """
    variables.separator()

    variables.message_loud("color bulb")

    if request.method == "POST":
        if "ip" in request.POST.keys() or "ip" in json.loads(request.body).keys():
            body = request.POST if "ip" in request.POST.keys() else json.loads(request.body)
            ip = body["ip"]

            m = variables.client.sender(
                ip,
                packet="turn_to_color",
                color_params={
                    "r": int(body["r"]),
                    "g": int(body["g"]),
                    "b": int(body["b"]),
                    "brightness": 255,
                },
            )
            if len(m) > 0:
                m = m[0]["result"]

                variables.message_loud(f"{ip} - {m}")

                variables.separator()
                return JsonResponse(m)
        variables.message_loud("Error, could not query bulb", "error")
        variables.separator()
        return JsonResponse({"error": "could not query bulb"})

    variables.separator()
    return render(request, "404.html", status=404)


def activate_music_sync(request) -> JsonResponse:
    """This will activate the music sync function of the application

    Args:
        request HttpRequest: HttpRequest object supplied by Django
    """
    variables.separator()
    variables.message_loud("Starting Audio Sync")

    if request.method == "POST" and request.body.decode("utf-8").isdigit():
        variables.message_loud(int(request.body.decode("utf-8")))
        audio_sync_thread = threading.Thread(
            target=audioSync, args=[int(request.body.decode("utf-8"))], daemon=True
        )
        try:
            variables.music_sync = True
            audio_sync_thread.start()
            pass
        except RuntimeError:
            pass

        sleep(30)
        if not audio_sync_thread.is_alive():
            variables.music_sync = False
            variables.separator()

        if not variables.music_sync:
            variables.message_loud("Audio Sync did not start", "error")
        variables.separator()
        return JsonResponse({"result": variables.music_sync})

    variables.separator()
    return render(request, "404.html", status=404)


def stop_audio_sync(request) -> JsonResponse:
    """Changes global variable to kill audio sync

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        JsonResponse: Returns true, as it stops the audio sync
    """
    variables.separator()

    if request.method == "POST":
        variables.message_loud("Stopping Audio Sync")
        variables.music_sync = False
        return JsonResponse({"result": True})

    variables.separator()
    return render(request, "404.html", status=404)


def crud(request) -> HttpResponse:
    """CRUD operations for the bulbs

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        HttpResponse: Renders 404 page if error
    """
    variables.separator()

    if request.method == "GET":
        variables.message_loud("load CRUD page")

        variables.context["ips"] = list(set(variables.context["ips"]))
        variables.separator()
        return render(request, "bulb_crud.html", variables.context)

    variables.separator()
    return render(request, "404.html", status=404)


def delete_bulb(request, ip):
    """CRUD operations for the bulbs

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        HttpResponse: renders crud page, with bulb deleted
    """
    variables.separator()
    if request.method == "POST":
        # Delete specific bulb
        variables.message_loud(f"Deleting bulb at {ip}")
        try:
            Wizbulb.objects.filter(bulb_ip=ip).delete()
            variables.context["bulbs"] = [
                x for x in variables.context["bulbs"] if x["bulb_ip"] != ip
            ]
            variables.context["success"] = True
            variables.context["successMessage"] = f"Deleted bulb at {ip}"

        except ValueError:
            variables.context["error"] = True
            variables.context["errorMessage"] = f"Error deleting bulb at {ip}"

        except Wizbulb.DoesNotExist:
            variables.context["error"] = True
            variables.context["errorMessage"] = "The bulb does not exist"

        variables.update_bulb_objects()
        variables.separator()
        return redirect("/crud/")

    variables.separator()
    return render(request, "404.html", status=404)


def edit_bulb(request, ip):
    """Edit specific bulb"""
    variables.separator()
    if request.method == "POST":
        variables.message_loud(f"Editing bulb at {ip}")
        try:
            form = BulbForm(request.POST)
            bulb = Wizbulb.objects.get(bulb_ip=ip)
            bulb.bulb_name = form.data["bulb_name"]
            bulb.bulb_ip = form.data["bulb_ip"]
            bulb.full_clean()
            bulb.save()

            variables.context["bulbs"] = []
            variables.update_bulb_objects()

            variables.context["success"] = True
            variables.context["successMessage"] = f"Successfully edited bulb at {ip}"

        except ValidationError as e:
            print(e)
            variables.context["error"] = True
            variables.context["errorMessage"] = "There was an error editing the bulb"

        except Wizbulb.DoesNotExist:
            variables.context["error"] = True
            variables.context["errorMessage"] = "The bulb does not exist"

        variables.update_bulb_objects()
        variables.separator()
        return redirect("/crud/")

    variables.separator()
    return render(request, "404.html", status=404)


def clear_error(request) -> JsonResponse:
    """Clears the success message from the context"""
    variables.separator()

    if request.method == "POST":
        variables.message_loud("Clearing error message")
        variables.separator()
        variables.context["error"] = False
        variables.context["errorMessage"] = ""
        return JsonResponse({"result": True})

    variables.separator()
    return render(request, "404.html", status=404)


def clear_success(request) -> JsonResponse:
    """Clears the success message from the context"""
    variables.separator()

    if request.method == "POST":
        variables.message_loud("Clearing success message")
        variables.separator()
        variables.context["success"] = False
        variables.context["successMessage"] = ""
        return JsonResponse({"result": True})

    variables.separator()
    return render(request, "404.html", status=404)


def faqs(request) -> HttpResponse:
    """Renders the FAQ page

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        HttpResponse: FAQ page
    """
    variables.separator()
    if request.method == "GET":
        variables.message_loud("load FAQ page")
        variables.separator()
        return render(request, "faq.html", variables.context)
    return render(request, "404.html", status=404)


def about(request) -> HttpResponse:
    """Renders the ABOUT page

    Args:
        request HttpRequest: HttpRequest object supplied by Django

    Returns:
        HttpResponse: ABOUT page
    """
    variables.separator()
    if request.method == "GET":
        variables.message_loud("load ABOUT page")
        variables.separator()
        return render(request, "about.html", variables.context)
    return render(request, "404.html", status=404)
