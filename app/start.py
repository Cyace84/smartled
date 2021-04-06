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





server.add_route("/", index)
server


""" start server """


server.start()
