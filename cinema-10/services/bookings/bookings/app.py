import queue
import threading
import time

from flask import Flask, jsonify
from werkzeug.exceptions import NotFound, TooManyRequests

import json
import os
import sys

app = Flask(__name__)

examples_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
sys.path.append(examples_path)
import helper
helper = helper.Helper("cinema-10")


with open("{}/cinema-10/services/bookings/bookings.json".format(examples_path), "r") as f:
    bookings = json.load(f)

q = queue.Queue()
MAX_QUEUE_SIZE = 5


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
    return jsonify({ "status": "OK" })


@app.route("/bookings", methods=['GET'])
def booking_list():
    return jsonify(bookings)


@app.route("/bookings/<username>", methods=['GET'])
def booking_record(username):
    # Basic load shedding.
    if q.qsize() > MAX_QUEUE_SIZE:
        print("queue size is: {}; aborting request.".format(str(q.qsize())))
        raise TooManyRequests

    print("current queue value: " + str(q.qsize()))

    # Put value in queue for client.
    q.put(True)

    # Sleep for a few seconds to simulate work.
    time.sleep(2)

    # Remove value from queue for client.
    q.get()

    if username not in bookings:
        raise NotFound
    return jsonify(bookings[username])


if __name__ == "__main__":
     app.run(port=helper.get_port('bookings'), host="0.0.0.0", debug=helper.get_debug(), threaded=True)
