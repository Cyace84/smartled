import time

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

modes = {
    "rainbow": "on"
}



def delete_task():
    modes["rainbow"] = "off"


#def wheel(pos):
#    # Input a value 0 to 255 to get a color value.
#    # The colours are a transition r - g - b - back to r.
#    if pos < 0 or pos > 255:
#        return (0, 0, 0)
#    if pos < 85:
#        return (255 - pos * 3, pos * 3, 0)
#    if pos < 170:
#        pos -= 85
#        return (0, 255 - pos * 3, pos * 3)
#    pos -= 170
#    return (pos * 3, 0, 255 - pos * 3)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return ( pos * 3, 255 - pos * 3, 0)
    if pos < 170:
        pos -= 85
        return ( 255 - pos * 3, 0, pos * 3)
    pos -= 170
    return (0, pos * 3,  255 - pos * 3)


def brightness_control(color, brightness=1):
    new_color = []
    for i in color:
        if i > i*brightness:
            new_color.append(int(i*brightness))
        else:
            new_color.append(i)

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


async def rainbow_cycle(n1, n2, slow=0):
    j = 0
    li = []
    print("start")
    while modes["rainbow"] == "on":
        j += 1
        roof1.fill((110,0,0))
        roof1.write()
        for i in range(n1, n2):
            rc_index = (i * 256 // 328) + j
            #roof1[i] = wheel(rc_index & 255)


        #li.append(time.time())
        await uasyncio.sleep_ms(10)
        roof1.fill((0,0,0))
        roof1.write()
        #if len(li) > 50:
        #    print(li[0], li[-1:])
        #    break

    return


loop = uasyncio.get_event_loop()
w = uasyncio.gather(
    rainbow_cycle(0,50),
    rainbow_cycle(50,100),
    rainbow_cycle(100,150),
    rainbow_cycle(150,200),
    rainbow_cycle(250,330),

)

loop.run_until_complete(w)
#uasyncio.run(main())
#uasyncio.run(rainbow_cycle(1,2))
#uasyncio.run(rainbow_cycle(1,2))
#create_task()
