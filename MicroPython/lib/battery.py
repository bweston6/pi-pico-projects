from machine import ADC, Pin
import time
import wlan
from wlan_credentials import WLAN_SSID, WLAN_PSK

_CONVERSION_FACTOR = 3 * 3.3 / 65535
_V_FULL = 4.2  # these are our reference voltages for a full/empty battery, in volts
_V_EMPTY = 2.8  # the values could vary by battery size/manufacturer so you might need to adjust them


@micropython.native
def voltage():
    wlan.disconnect()
    vsysEn = Pin(25, Pin.OUT)
    vsysEn.on()
    # wait to become stable
    time.sleep(0.01)
    # take average of 5
    voltage = 0
    for i in range(5):
        voltage += ADC(29).read_u16() * _CONVERSION_FACTOR
    voltage /= 5
    vsysEn.off()
    return voltage


@micropython.native
def percent():
    percentage = 100 * ((voltage() - _V_EMPTY) / (_V_FULL - _V_EMPTY))
    return percentage


@micropython.native
def charging():
    charging = False
    if voltage() > 4.5:
        charging = True
    return charging
