import time

import machine, neopixel
import _thread as thread
roof1 = neopixel.NeoPixel(machine.Pin(4), 330)
roof2 = neopixel.NeoPixel(machine.Pin(5), 330)
tg1 = neopixel.NeoPixel(machine.Pin(19), 149)
tg2 = neopixel.NeoPixel(machine.Pin(21), 149)
tg3 = neopixel.NeoPixel(machine.Pin(22), 149)
tg4 = neopixel.NeoPixel(machine.Pin(23), 149)

modes = {
    "rainbow": "on"
}



def delete_task():
    modes["rainbow"] = "off"


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

def brightness_control(color, brightness=1):
    new_color = []
    for i in color:
        if i > i*brightness:
            new_color.append(int(i*brightness))
        else:
            new_color.append(i)

    return tuple(new_color)

pin2 = machine.Pin(2, machine.Pin.OUT)


def rainbow_cycle(slow=0):
    j = 0
    while modes["rainbow"] == "on":
        j += 1
        for i in range(30):
            rc_index = (i * 256 // 328) + j
            roof1[i] = brightness_control(wheel(rc_index & 255), brightness=0.5)
        time.sleep(slow)
        roof1.write()

    return



def create_task():
    thread.start_new_thread(rainbow_cycle, ())

