import time
import random
import machine
import _thread as thread
from esp import neopixel_write
import uasyncio

class NeoPixel:
    ORDER = (1, 0, 2, 3)
    __slots__ = ("pin", "n", "bpp", "buf", "timing")

    def __init__(self, pin, n, bpp=3, timing=1):
        self.pin = pin
        self.n = n
        self.bpp = bpp
        self.buf = bytearray(n * bpp)
        self.pin.init(pin.OUT)
        self.timing = timing

    def __setitem__(self, index, val):
        offset = index * self.bpp
        for i in range(self.bpp):
            self.buf[offset + self.ORDER[i]] = val[i]

    def __getitem__(self, index):
        offset = index * self.bpp
        return tuple(self.buf[offset + self.ORDER[i]] for i in range(self.bpp))

    def fill(self, color):
        for i in range(self.n):
            self[i] = color

    def write(self):
        neopixel_write(self.pin, self.buf, self.timing)

roof1 = NeoPixel(machine.Pin(4), 330)
roof2 = NeoPixel(machine.Pin(5), 330)
tg1 = NeoPixel(machine.Pin(19), 149)
tg2 = NeoPixel(machine.Pin(21), 149)
tg3 = NeoPixel(machine.Pin(22), 149)
tg4 = NeoPixel(machine.Pin(23), 149)

strip_dict = {
    "roof1": roof1,
    "roof2": roof2,
    "ledCorner1": tg1,
    "ledCorner2": tg2,
    "ledCorner3": tg3,
    "ledCorner4": tg4
}

modes = {
    "rainbow": "off",
    "fireflicker": "off"
}




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
        new_color.append(int(i*brightness))

    return tuple(new_color)

pin2 = machine.Pin(2, machine.Pin.OUT)


def set_color(j):
    #lis = bytearray(330*3)
    ORDER = (1, 0, 2, 3)
    #for i in range(330):
        #offset = i * 3
        #rc_index = (i * 256 // 328) + j
        #color = wheel(rc_index & 255)
        #lis[i]  = 255
        #for s in range(3):
        #    lis[offset + ORDER[s]] = color[s]
    l = [wheel(i * 256 // 328 + j & 255) for i in range(330)]
    l = str(l).replace("(", "").replace(")", "")

    return bytearray(eval(l))

async def rainbow_cycle(strips, color, brightness, speed):
    j = 0
    li = []
    _delay = {
        0: 0,
        1: random.randint(50,100),
        2: random.randint(100,250),
        3: random.randint(250,350),
        4: random.randint(350,600),
        5: random.randint(600,800),
        6: random.randint(800,1000)
        }
    while modes["rainbow"] == "on":
        j += 1

        for strip in strips:
            leds = [i for i in range(strip.n)]
            if strip in [tg1, tg2, tg3, tg4]:
                leds = [q for q in range(strip.n)]
                leds.reverse()

            for i in leds:
                rc_index = (i * 256 // 328) + j
                strip[i] = brightness_control(wheel(rc_index & 255), brightness)

        await uasyncio.sleep_ms(_delay[speed])
        for i in strips:
            i.write()


    return


async def fireflicker_cycle(strips, speed, color, brightness):
    #  Regular (orange) flame:

    if color == "orange":
        r = 226
        g = 121
        b = 35
    elif color == "purple":
        r = 158
        g = 8
        b = 148
    elif color == "green":
        r = 74
        g = 150
        b = 12

    _delay = {
        0: 0,
        1: random.randint(50,100),
        2: random.randint(100,250),
        3: random.randint(250,350),
        4: random.randint(350,600),
        5: random.randint(600,800),
        6: random.randint(800,1000)
        }
    s=[]

    while modes["fireflicker"] == "on":
        for i in strips:

            leds = range(i.n)
            if i in [tg1, tg2, tg3, tg4]:
                leds = [q for q in range(i.n)]
                leds.reverse()
            ss = []
            for r in leds:
                flicker = random.randint(0,55)
                r1 = r - flicker
                g1 = g - flicker
                b1 = b - flicker

                r1 = r1 if r1 > 0 else 0
                g1 = g1 if g1 > 0 else 0
                b1 = b1 if b1 > 0 else 0

                i[r] = brightness_control((r1, g1, b1), brightness)
                ss.append((r1, g1, b1))
            i.write()


        await uasyncio.sleep_ms(_delay[speed])
        for i in strips:
            i.write()



def bonfire_cycle(strip):
    if color == "orange":
        r = 226
        g = 121
        b = 0
    elif color == "purple":
        r = 158
        g = 8
        b = 148
    elif color == "green":
        r = 74
        g = 150
        b = 12

    while modes["bonfire"] == "on":
        for i in range(150):
            strip[i] = brightness_control((r1, g1, b1), brightness)
            strip.write()




loop2 = uasyncio.get_event_loop()


def create_task(mode_name, strips, color, brightness, speed):

    _strips = []
    if modes[mode_name] == "on":
        modes[mode_name] = "off"
        return

    modes[mode_name] = "on"

    for strip in strips:
        if strip == "roofAll":
            _strips.extend([roof1, roof2])
        elif strip == "cornersAll":
            _strips.extend([tg1, tg2, tg3, tg4])
        else:
            _strips.append(strip_dict[strip])
    if mode_name == "fireflicker":
        w = uasyncio.gather(fireflicker_cycle(_strips, color=color, brightness=brightness, speed=speed))
        loop2.run_until_complete(w)
    print(mode_name)
    if mode_name == "rainbow":
        print(1)
        w = uasyncio.gather(rainbow_cycle(_strips, color=color, brightness=brightness, speed=speed))
        loop2.run_until_complete(w)


if __name__ == "__main__":
    pass

