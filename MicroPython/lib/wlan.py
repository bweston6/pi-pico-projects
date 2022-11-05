import network
import time

wlan = network.WLAN(network.STA_IF)


def connect(ssid, psk):
    print("wlan: connecting to " + ssid)
    wlan.active(True)
    wlan.connect(ssid, psk)
    while wlan.status() != network.STAT_GOT_IP:
        pass
    ip = wlan.ifconfig()[0]
    print("wlan: connected as " + ip)


def disconnect():
    if wlan.isconnected():
        print("wlan: disconnecting")
    wlan.disconnect()
    wlan.active(False)
    wlan.deinit()


def isconnected():
    return wlan.isconnected()


def active(state=None):
    if state == None:
        return wlan.active()
    wlan.active(state)
