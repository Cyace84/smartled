import esp
import network
import time
import socket
import sys
import io
import os
import uasyncio
import machine, NeoPixel
import re

from app import secrets

wlan_id = secrets.WIFI_SSID
wlan_pass = secrets.WIFI_PASSWORD

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


from app.micropyserver import MicroPyServer

server = MicroPyServer()
""" add request handler """


def index(request, data):
    """ request handler """
    response = __import__("templates").index
    server.send(response)


np1 = neopixel.NeoPixel(machine.Pin(2), 50)
np2 = neopixel.NeoPixel(machine.Pin(4), 50)
np3 = neopixel.NeoPixel(machine.Pin(5), 50)
np4 = neopixel.NeoPixel(machine.Pin(19), 50)
np5 = neopixel.NeoPixel(machine.Pin(21), 50)
np6 = neopixel.NeoPixel(machine.Pin(23), 50)

np1[0] = (0,0,255)
np2[0] = (0,220,0)
np3[0] = (0,0,220)
np4[0] = (50,0,0)
np5[0] = (0,50,0)
np6[0] = (0,0,50)

np1.clear()
np2.clear()
np3.clear()
np4.clear()
np5.clear()
np6.clear()


server.add_route("/", index)
server


""" start server """


server.start()
