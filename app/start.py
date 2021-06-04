import esp
import network
import time
import socket
import sys
import io
import os
import uasyncio
import machine, neopixel
import re
import random
from app import secrets

wlan_id = secrets.WIFI_SSID#"TP-LINK_0876"#
wlan_pass = secrets.WIFI_PASSWORD#"45275838"#

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if wlan.isconnected() == False:
    wlan.connect(wlan_id, wlan_pass)
    sleep = 0
    while wlan.isconnected() == False:
        time.sleep(1)
        sleep += 1
        if sleep > 10:
            wlan.connect("default", "12345678")
print("Device IP:", wlan.ifconfig()[0])

pin2 = machine.Pin(2, machine.Pin.OUT)



from app.micropyserver import MicroPyServer

server = MicroPyServer()
""" add request handler """

def parse_data(data):
    data = data.replace("%5B%5D", "[]").replace("+", "").replace("%2C", ",").replace("rgb", "").split("&")
    new_data = {"strips": []}
    for i in data:
        print(data)
        k = i.split("=")[0]
        v = i.split("=")[1]
        if k == "color":
            new_data["color"] = eval(v)

        if k == "strips":
            new_data["strips"].append(v)

    return new_data


def index(request, q):
    """ request handler """
    pin2.on()
    time.sleep(1)
    pin2.off()

    response = "{}".format(wlan.ifconfig()[0])
    data = parse_data(request.split("\r\n\r\n")[-1])
    if data.get("color"):
        set_color(data)
    server.send(response)


roof1 = neopixel.NeoPixel(machine.Pin(4), 330)
roof2 = neopixel.NeoPixel(machine.Pin(5), 330)
tg1 = neopixel.NeoPixel(machine.Pin(19), 149)
tg2 = neopixel.NeoPixel(machine.Pin(21), 149)
tg3 = neopixel.NeoPixel(machine.Pin(22), 149)
tg4 = neopixel.NeoPixel(machine.Pin(23), 149)

pin2.on()
time.sleep(5)
pin2.off()


roof1.fill((120,0,0))
roof2.fill((0, 120, 0))
tg1.fill((0, 120, 120))
tg2.fill((120, 120, 0))
tg3.fill((120, 0, 120))
tg4.fill((50, 120, 0))


roof1[10] = (255,0,0)
roof1.write()
def _set_color(pin_parent, pin, color: tuple):

    for i in strips[pin]:
        pin_parent[i] = color
    pin_parent.write()


strips = {
            "roof1": roof1[:179],
            "roof2": roof1[179:],
            "roof3": roof2[:176],
            "roof4": roof2[176:],
            "corner1": tg1,
            "corner2": tg2,
            "corner3": tg3,
            "corner4": tg4
        }

def set_color(data):
    for led in data["strips"]:
        color = data["color"]
        if led == "cornerAll":
            tg1.fill(color)
            tg2.fill(color)
            tg3.fill(color)
            tg4.fill(color)
        elif led == "roofAll":
            roof1.fill(color)
            roof2.fill(color)
        else:
            if led[:4] == "roof":
                if led in ["roof1", "roof2"]:
                    _set_color(roof1, led, color)
                else:
                    _set_color(roof2, led, color)
            else:
                strips[led].fill(color)






server.add_route("/", index)



""" start server """
for i in range(3):
    time.sleep(0.5)

    pin2.on()
    time.sleep(1)
    pin2.off()

server.start()
