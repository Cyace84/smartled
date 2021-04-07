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
num_pixels=330
pixel_pin = machine.Pin(4)

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, timing=0)
st134 = neopixel.NeoPixel(machine.Pin(5), 327)
tg1 = neopixel.NeoPixel(machine.Pin(19), 149)
tg2 = neopixel.NeoPixel(machine.Pin(21), 149)
tg3 = neopixel.NeoPixel(machine.Pin(22), 149)
tg4 = neopixel.NeoPixel(machine.Pin(23), 149)


def set_color(pin, color: tuple):
    for i in range(pin.n):
        pin[i] = color
    pin.write()

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.write()
        time.sleep(0.5)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.write()



RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

while True:
    pixels.fill(RED)
    pixels.write()
    # Increase or decrease to change the speed of the solid color change.
    time.sleep(1)
    pixels.fill(GREEN)
    pixels.write()
    time.sleep(1)
    pixels.fill(BLUE)
    pixels.write()
    time.sleep(1)

    color_chase(RED, 0.1)  # Increase the number to slow down the color chase
    color_chase(YELLOW, 0.1)
    color_chase(GREEN, 0.1)
    color_chase(CYAN, 0.1)
    color_chase(BLUE, 0.1)
    color_chase(PURPLE, 0.1)

    rainbow_cycle(0)  # Increase the number to slow down the rainbow

server.add_route("/", index)
server


""" start server """


server.start()
