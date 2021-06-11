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
#from app import secrets
pin2 = machine.Pin(2, machine.Pin.OUT)
pin2.on()
time.sleep(2)
pin2.off()

from micropyserver import MicroPyServer


from app.dynamic import create_task
from app.micropyserver import MicroPyServer

wlan_id = "TP-LINK_3EA72E"#secrets.WIFI_SSID#"TP-LINK_0876"#
wlan_pass = "20627653"#secrets.WIFI_PASSWORD#"45275838"#

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

pin2.on()
time.sleep(2)
pin2.off()





server = MicroPyServer()
""" add request handler """

def parse_data(data):
    data = data.replace("%5B%5D", "").replace("+", "").replace("%2C", ",").replace("rgb", "").split("&")
    new_data = {"strips": []}
    for i in data:
        k = i.split("=")[0]
        v = i.split("=")[1]
        if k == "color":
            new_data["color"] = eval(v)

        if k == "strips":
            new_data["strips"].append(v)

    return new_data




roof1 = neopixel.NeoPixel(machine.Pin(4), 330)
roof2 = neopixel.NeoPixel(machine.Pin(5), 330)
tg1 = neopixel.NeoPixel(machine.Pin(19), 149)
tg2 = neopixel.NeoPixel(machine.Pin(21), 149)
tg3 = neopixel.NeoPixel(machine.Pin(22), 149)
tg4 = neopixel.NeoPixel(machine.Pin(23), 149)



roof1.fill((0,0,0))
roof2.fill((0,0,0))
tg1.fill((0,0,0))
tg2.fill((0,0,0))
tg3.fill((0,0,0))
tg4.fill((0,0,0))

#for i in range(76):
#    tg1[i] = (0, 87, 184)


#for i in range(76, 149):

#    tg1[i] = (255, 216, 0)

roof1.write()
roof2.write()
tg1.write()
tg2.write()
tg3.write()
tg4.write()

import _thread


def _set_color(pin_parent, pin, color: tuple):

    for i in strips[pin]:
        pin_parent[i] = color
    pin_parent.write()


strips = {
            "ledRoof1": range(0, 179),
            "ledRoof2": range(179, 330),
            "ledRoof3": range(0, 151),
            "ledRoof4": range(151, 330),
            "ledCorner1": tg1,
            "ledCorner2": tg2,
            "ledCorner3": tg3,
            "ledCorner4": tg4
        }

def set_color(data):
    for led in data["strips"]:
        color = data["color"]
        if led == "cornersAll":
            tg1.fill(color)
            tg2.fill(color)
            tg3.fill(color)
            tg4.fill(color)
            tg1.write()
            tg2.write()
            tg3.write()
            tg4.write()
        elif led == "roofAll":
            roof1.fill(color)
            roof2.fill(color)
            roof1.write()
            roof2.write()
        else:

            if led[3:-1] == "Roof":
                if led in ["ledRoof1", "ledRoof2"]:
                    _set_color(roof1, led, color)
                else:
                    _set_color(roof2, led, color)
            else:
                strips[led].fill(color)
                strips[led].write()


def index(request, q):
    """ request handler """

    #response = "{}".format(wlan.ifconfig()[0])
    data = parse_data(request.split("\r\n\r\n")[-1])
    if data.get("color"):
        set_color(data)
        dynamic.delete_task()
    server.send("wqeqweq")


server.add_route("/", index)



""" start server """

pin2.on()
time.sleep(2)
pin2.off()
def ww():
    server.start()
_thread.start_new_thread(ww, ())

_thread.start_new_thread(create_task, ("flame"))
