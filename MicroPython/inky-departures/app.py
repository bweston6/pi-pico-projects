from flask import Flask, jsonify, request
import requests
import re

app = Flask(__name__)

_URL = "https://nextbuses.mobi/WebView/BusStopSearch/BusStopSearchResults/%s"


@app.route("/", methods=["GET"])
def getBus():
    stopIds = request.args.getlist("stopId")
    responses = []
    for stopId in stopIds:
        page = requests.get(_URL % stopId).text
        table = re.search(r"<table.*>((.|\n)*?)</table>", page, re.MULTILINE).group(1)
        busses = re.findall(r"<tr>((.|\n)*?)</tr>", table, re.MULTILINE)

        response = []
        for bus in busses:
            bus = bus[0]
            route = re.search(r"<p.*>(.*)</a>", bus, re.MULTILINE).group(1)
            arrivalTime = re.search(
                r"<p.*(?:at |in )(.*)</p>", bus, re.MULTILINE
            ).group(1)
            response.append({"route": route, "arrivalTime": arrivalTime})
        responses.append(response)

    return jsonify(responses)
