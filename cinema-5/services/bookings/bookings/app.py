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
helper = helper.Helper("cinema-5")


with open("{}/cinema-5/services/bookings/bookings.json".format(examples_path), "r") as f:
    bookings = json.load(f)


@app.route("/", methods=['GET'])
def hello():
    return jsonify({
        "uri": "/",
        "subresource_uris": {
            "bookings": "/bookings",
            "booking": "/bookings/<username>"
        }
    })


@app.route("/health-check", methods=['GET'])
def bookings_health_check():
    return jsonify({"status": "OK"})


@app.route("/bookings", methods=['GET'])
def booking_list():
    return jsonify(bookings)


@app.route("/bookings/<username>", methods=['GET'])
def booking_record(username):
    if username not in bookings:
        raise NotFound
    return jsonify(bookings[username])


if __name__ == "__main__":
    app.run(port=helper.get_port('bookings'),
            host="0.0.0.0", debug=helper.get_debug())
