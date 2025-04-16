import helper
from flask import Flask, jsonify
from werkzeug.exceptions import NotFound, ServiceUnavailable

import json
import os
import sys
import requests

app = Flask(__name__)

examples_path = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
sys.path.append(examples_path)
helper = helper.Helper("cinema-8")


@app.route("/health-check", methods=['GET'])
def api_server_health_check():
    return jsonify({"status": "OK"})


@app.route("/users/<username>/bookings", methods=['GET'])
def api_server_record(username):
    RETRIES = 2

    for i in range(0, RETRIES):
        try:
            users_bookings = requests.get("http://{}:{}/users/{}/bookings".format(helper.resolve_requests_host(
                'monolith'), helper.get_port('monolith'), username), timeout=helper.get_timeout('monolith'))
            if users_bookings.status_code == 200:
                break

        except requests.exceptions.ConnectionError:
            if i == RETRIES - 1:
                raise ServiceUnavailable("The monolith is unavailable.")
        except requests.exceptions.Timeout:
            if i == RETRIES - 1:
                raise ServiceUnavailable("The monolith timed out.")

    if users_bookings.status_code == 404:
        raise NotFound("No bookings were found for {}".format(username))

    if users_bookings.status_code != 200:
        raise ServiceUnavailable("The Bookings service is malfunctioning.")

    users_bookings = users_bookings.json()

    return jsonify(users_bookings)


if __name__ == "__main__":
    app.run(port=helper.get_port('api-server'),
            host="0.0.0.0", debug=helper.get_debug())
