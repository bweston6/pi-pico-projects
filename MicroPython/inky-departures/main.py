from picographics import PicoGraphics, DISPLAY_INKY_PACK
from wlan_credentials import WLAN_SSID, WLAN_PSK
import battery
import machine
import time
import web_time
import wlan
import gc
import urequests

import micropython
micropython.alloc_emergency_exception_buf(100)


_SERVER = const("http://bus.bweston.uk/?%s")
_STOP1 = const("merdjmjd")
_STOP2 = const("merdjmjg")
_STOP3 = const("cordmptj")
_STOPS = [_STOP1, _STOP2, _STOP3]

@micropython.viper
def btnHandler(pin):
    global stop
    # debounce
    pin.irq(handler=None)
    machine.Timer(mode=machine.Timer.ONE_SHOT, period=1000, callback=enableButtons)
    if pin == btnA:
        stop = 0
    elif pin == btnB:
        stop = 1
    else:
        stop = 2
    micropython.schedule(updateDisplay, None)


def getData(*_):
    global busses
    wlan.connect(WLAN_SSID, WLAN_PSK)
    query = ""
    for stop in _STOPS:
        query += "stopId=%s&" % stop
    url = _SERVER % query
    print(url)
    _error_count = 0
    for i in range(3):
        try:
            print("data: fetching new data")
            r = urequests.get(url, timeout=20)
            busses = r.json()
            r.close()
        except OSError as e:
            print(e)
            if e.errno == errno.ETIMEDOUT:
                _error_count += 1
                if _error_count == 3:
                    machine.reset()
            continue
        else:
            break
    print("data: data aquired")
    wlan.disconnect()
    updateDisplay()


def getBattery(*_):
    global batteryPercent
    batteryPercent = round(battery.voltage(), 1)


def updateDisplay(*args):
    # clear display
    display.set_pen(15)
    display.clear()
    # draw head
    display.set_pen(0)
    display.rectangle(0, 0, head, h)
    display.set_pen(15)
    time = rtc.datetime()
    hour = time[4]
    if time[5] < 10:
        minute = "0" + str(time[5])
    else:
        minute = time[5]
    textWidth = display.measure_text(
        str(hour) + ":" + str(minute) + " " + str(batteryPercent) + "v", scale=0.7
    )
    display.text(
        str(hour) + ":" + str(minute) + " " + str(batteryPercent) + "v",
        int(head / 2),
        int(h / 2 + textWidth / 2),
        scale=0.7,
        angle=270,
    )
    # draw foot

    # draw table
    display.set_pen(0)
    display.rectangle(head, int(2 * h / 3), w - head, int(h / 3 + 1))
    display.set_pen(0)
    for x in range(1, 5):
        display.line(
            int((w - head) / 5 * x + head), 0, int((w - head) / 5 * x + head), h
        )
    for count, bus in enumerate(busses[stop][:5]):
        # route
        display.set_pen(15)
        textWidth = display.measure_text(bus["route"], scale=0.7)
        textOffset = int(h - (h / 3 - textWidth) / 2)
        display.text(
            bus["route"],
            int((w - head) / 5 * count + (w - head) / 10 + head),
            textOffset,
            scale=0.7,
            angle=270,
        )
        # arrivalTime
        display.set_pen(0)
        scale = 0.8
        textWidth = display.measure_text(bus["arrivalTime"], scale=scale)
        while textWidth > 2 * h / 3:
            scale -= 0.05
            textWidth = display.measure_text(bus["arrivalTime"], scale=scale)
        textOffset = int(2 * h / 3 - (2 * h / 3 - textWidth) / 2)
        display.text(
            bus["arrivalTime"],
            int((w - head) / 5 * count + (w - head) / 10 + head),
            textOffset,
            scale=scale,
            angle=270,
        )
    if len(args) > 0 and args[0] is not None:
        print("display: updating head")
        display.partial_update(0, 0, head, h)
    else:
        print("display: updating display")
        display.update()

wlan.disconnect()
machine.Pin("LED", machine.Pin.OUT).on()
print("main: board reset")


# setup display
display = PicoGraphics(display=DISPLAY_INKY_PACK)
display.set_font("sans")
head = 18
foot = 0
w, h = display.get_bounds()
display.set_update_speed(2)


# get battery before WiFi init
getBattery()


# initialise variables
stop = 0
busses = [[], [], []]


# set time
rtc = machine.RTC()
updateDisplay()
web_time.init(rtc)
updateDisplay(True)


# setup button handlers
btnA = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
btnB = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
btnC = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

def enableButtons(*_):
    btnA.irq(trigger=machine.Pin.IRQ_FALLING, handler=btnHandler)
    btnB.irq(trigger=machine.Pin.IRQ_FALLING, handler=btnHandler)
    btnC.irq(trigger=machine.Pin.IRQ_FALLING, handler=btnHandler)

enableButtons()


while True:
    getData()
    for i in range(4):
        updateDisplay(True)
