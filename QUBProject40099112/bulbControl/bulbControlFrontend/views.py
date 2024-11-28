from django.shortcuts import render, redirect
from django.utils.safestring import SafeString
from django.http import JsonResponse
from .forms import bulbForm
from .models import wizBulb
from socket import *
from time import sleep
from time import time_ns
import json
from .helpers import sendUDPPacket, updateBulbObjects

discover = b"{\"method\":\"getPilot\",\"params\":{}}"
turn_on = b"{\"id\":1,\"method\":\"setState\",\"params\":{\"state\":true}}"
turn_off = b"{\"id\":1,\"method\":\"setState\",\"params\":{\"state\":false}}"
port = 38899


def index(request):
    # To add a limit to the returned bulb objects the line would read bulbs = wizBulb.objects.all()[x] where x is the number of bulb objects returned
    bulbs = wizBulb.objects.all()
    context = {'regForm': bulbForm(), 'ips': [], 'count': 0,
               'bulbs': [], 'numBulbs': 0}
    for x in bulbs:
        updateBulbObjects(x)
        context['bulbs'].append(x.returnJSON())

    print('-' * 20)
    if request.method == 'POST':

        # Discover bulbs on network
        if 'discover' in request.POST.keys():
            print('discover')
            sock = socket(AF_INET, SOCK_DGRAM)
            sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
            sock.bind(('', port))
            sock.settimeout(0.5)
            sock.sendto(discover, ('255.255.255.255', port))
            m = sock.recvfrom(516)
            count = 0
            while m != None:
                if m[0] != discover:
                    bulbResponse = json.loads(m[0].decode('utf-8'))
                    print(json.dumps(bulbResponse['result']))

                    context['count'] = range(count)
                    context['ips'].append(str(m[1]).replace(
                        '(', '').replace("'", "").split(",", maxsplit=1)[0])
                    count += 1
                try:
                    m = sock.recvfrom(516)
                except Exception:
                    m = None

            print(context)
            print('-' * 20)

            sock.close()
            context['numBulbs'] = len(context['bulbs'])
            return render(request, 'index.html', context)

            # Create bulb object in db
        else:
            print('form')
            m = sendUDPPacket(request.POST['bulbIp'], port, discover)
            bulbResponse = json.loads(m[0].decode('utf-8'))['result']
            form = bulbForm(request.POST)
            print("Form: ")
            print(form)
            if form.is_valid():
                model = form.save(commit=False)
                model.bulbState = bulbResponse['state']
                model.bulbRed = bulbResponse['r'] if 'r' in bulbResponse.keys(
                ) else 0
                model.bulbGreen = bulbResponse['g'] if 'g' in bulbResponse.keys(
                ) else 0
                model.bulbBlue = bulbResponse['b'] if 'b' in bulbResponse.keys(
                ) else 0
                model.bulbTemp = bulbResponse['temp'] if 'temp' in bulbResponse.keys(
                ) else 0
                model.save()
                bulbs = wizBulb.objects.all()
                for x in bulbs:
                    updateBulbObjects(x)
                    context['bulbs'].append(x.returnJSON())
                context['numBulbs'] = len(context['bulbs'])
                return render(request, 'index.html', context)
            else:
                context['numBulbs'] = len(context['bulbs'])
                return render(request, 'index.html', context)

    elif request.method == 'GET':
        print(request.GET)
        print("load home page")
        print('-' * 20)

        context['numBulbs'] = len(context['bulbs'])
        return render(None, 'index.html', context)


def toggleBulb(request):
    if request.method == 'POST':
        print(request.POST)

        # Flicker specific bulb
        if 'ip' in request.POST.keys() or 'ip' in json.loads(request.body.decode('utf-8')).keys():
            print("toggle")
            ip = request.POST['ip'] if 'ip' in request.POST.keys(
            ) else json.loads(request.body.decode('utf-8'))['ip']
            print('-' * 20)
            startTime = time_ns()
            m = json.loads(sendUDPPacket(ip, port, discover)
                           [0].decode("utf-8"))['result']
            endTime = time_ns()
            totalTime = (endTime - startTime) / 1000000000
            print("Toggle time: " + str(totalTime))
            if m['state']:
                sendUDPPacket(ip, port, turn_off)
                m = json.loads(sendUDPPacket(ip, port, discover)
                               [0].decode("utf-8"))['result']
                return JsonResponse(m)
            else:
                sendUDPPacket(ip, port, turn_on)
                m = json.loads(sendUDPPacket(ip, port, discover)
                               [0].decode("utf-8"))['result']
                return JsonResponse(m)


def queryBulb(request):
    if request.method == 'POST':
        print(request.POST)
        body = json.loads(request.body.decode(
            'utf-8')) if request.body else None
        # Flicker specific bulb
        if 'ip' in request.POST.keys() or 'ip' in body.keys():
            print("query bulb")
            ip = request.POST['ip'] if 'ip' in request.POST.keys(
            ) else body['ip']
            print('-' * 20)

            m = json.loads(sendUDPPacket(ip, port, discover)
                           [0].decode("utf-8"))['result']
            if m['state']:
                return JsonResponse(m)
            else:
                return JsonResponse(m)
