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


st123 = neopixel.NeoPixel(machine.Pin(4), 330)
st134 = neopixel.NeoPixel(machine.Pin(5), 327)
tg1 = neopixel.NeoPixel(machine.Pin(19), 149)
tg2 = neopixel.NeoPixel(machine.Pin(21), 149)
tg3 = neopixel.NeoPixel(machine.Pin(22), 149)
tg4 = neopixel.NeoPixel(machine.Pin(23), 149)


async def set_color(pin, color: tuple):
    for i in range(pin.n):
        pin[i] = color
    print(1)
    await pin.write()

set_color



""" start server """


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


st123 = neopixel.NeoPixel(machine.Pin(4), 330)
st134 = neopixel.NeoPixel(machine.Pin(5), 327)
tg1 = neopixel.NeoPixel(machine.Pin(19), 149)
tg2 = neopixel.NeoPixel(machine.Pin(21), 149)
tg3 = neopixel.NeoPixel(machine.Pin(22), 149)
tg4 = neopixel.NeoPixel(machine.Pin(23), 149)


def set_color(pin, color: tuple):
    for i in range(pin.n):
        pin[i] = color
    pin.write()

def demo(np):
    n = np.n


    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()

demo(st123)

server.add_route("/", index)
server


""" start server """


server.start()
