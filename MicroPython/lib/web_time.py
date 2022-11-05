from wlan_credentials import WLAN_SSID, WLAN_PSK
import re
import urequests
import wlan
import machine
import errno

_URL = "https://worldtimeapi.org/api/ip"


def init(rtc):
    # connect to wifi
    wlan.connect(WLAN_SSID, WLAN_PSK)
    _error_count = 0
    while True:
        try:
            print("web_time: fetching time")
            r = urequests.get(_URL, timeout=20)
        except OSError as e:
            print(e)
            if e.errno == errno.ETIMEDOUT:
                _error_count += 1
                if _error_count == 3:
                    machine.reset()
            continue
        else:
            break

    json = r.json()
    r.close()
    print("web_time: request received")
    match = re.match(
        "^(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d).(\d\d).*$", json["datetime"]
    )
    time = list(match.groups())
    time = [int(x) for x in time]
    time.insert(3, json["day_of_week"])
    time = tuple(time)
    rtc.datetime(time)
    print("web_time: time set")