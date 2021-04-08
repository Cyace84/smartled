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
num_pixels=330
pixel_pin = machine.Pin(4)

st123 = neopixel.NeoPixel(pixel_pin, 330)
st134 = neopixel.NeoPixel(machine.Pin(5), 327)
tg1 = neopixel.NeoPixel(machine.Pin(19), 149)
tg2 = neopixel.NeoPixel(machine.Pin(21), 149)
tg3 = neopixel.NeoPixel(machine.Pin(22), 149)
tg4 = neopixel.NeoPixel(machine.Pin(23), 149)


def set_color(pin, color: tuple):
    for i in range(pin.n):
        pin[i] = color
    pin.write()


while True:
    st123.fill((0,0,0))
    st134.fill((0,0,0))
    for i in range(st123.n):

        st123[i] = (0, 20, 0)
        st123.write()

        st134[i] = (random.randint(0, 60),random.randint(0, 60),random.randint(0, 60))
        st134.write()

server.add_route("/", index)
server


""" start server """


server.start()
