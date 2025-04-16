import helper
from flask import Flask, jsonify
from werkzeug.exceptions import NotFound

import json
import os
import sys

app = Flask(__name__)

examples_path = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
sys.path.append(examples_path)
helper = helper.Helper("cinema-12")


with open("{}/cinema-12/services/showtimes/showtimes.json".format(examples_path), "r") as f:
    showtimes = json.load(f)


@app.route("/", methods=['GET'])
def hello():
    return jsonify({
        "uri": "/",
        "subresource_uris": {
            "showtimes": "/showtimes",
            "showtime": "/showtimes/<date>"
        }
    })


@app.route("/health-check", methods=['GET'])
def showtimes_health_check():
    return jsonify({"status": "OK"})


@app.route("/showtimes", methods=['GET'])
def showtimes_list():
    return jsonify(showtimes)


@app.route("/showtimes/<date>", methods=['GET'])
def showtimes_record(date):
    if date not in showtimes:
        raise NotFound
    return jsonify(showtimes[date])


if __name__ == "__main__":
    app.run(port=helper.get_port('showtimes'), host="0.0.0.0",
            debug=helper.get_debug(), threaded=True)
