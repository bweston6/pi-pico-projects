import WIFI_CONFIG
from network_manager import NetworkManager
import uasyncio
from urllib import urequest
from picographics import PicoGraphics, DISPLAY_INKY_PACK
import jpegdec
import random
import time


"""
Grab a random image from PlaceKitten.com
and display it on Inky Pack.

Optionally cache to flash, if you need the RAM
for something else.
"""


graphics = PicoGraphics(DISPLAY_INKY_PACK)
WIDTH, HEIGHT = graphics.get_bounds()
FILENAME = "placekitten.jpg"
ENDPOINT = "http://placekitten.com/{0}/{1}"


def status_handler(mode, status, ip):
    graphics.set_pen(15)
    graphics.clear()
    graphics.set_pen(0)
    graphics.text("Network: {}".format(WIFI_CONFIG.SSID), 10, 10, scale=2)
    status_text = "Connecting..."
    if status is not None:
        if status:
            status_text = "Connection successful!"
        else:
            status_text = "Connection failed!"
    graphics.text(status_text, 10, 30, scale=2)
    graphics.text("IP: {}".format(ip), 10, 60, scale=2)
    graphics.update()


graphics.set_font("bitmap8")
network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)
uasyncio.get_event_loop().run_until_complete(
    network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK)
)
data = bytearray(1024 * 10)


while True:
    url = ENDPOINT.format(WIDTH + random.randint(0, 10), HEIGHT + random.randint(0, 10))
    print("Requesting URL: {}".format(url))
    socket = urequest.urlopen(url)
    socket.readinto(data)
    socket.close()

    jpeg = jpegdec.JPEG(graphics)
    jpeg.open_RAM(data)
    jpeg.decode(0, 0)
    graphics.update()

    time.sleep(10)
