import helper
from flask import Flask, jsonify
from werkzeug.exceptions import NotFound, ServiceUnavailable

import json
import requests
import os
import sys

app = Flask(__name__)

helper = helper.Helper("cinema-2")


with open("users.json", "r") as f:
    users = json.load(f)


@app.route("/", methods=['GET'])
def hello():
    return jsonify({
        "uri": "/",
        "subresource_uris": {
            "users": "/users",
            "user": "/users/<username>",
            "bookings": "/users/<username>/bookings",
            "suggested": "/users/<username>/suggested"
        }
    })


@app.route("/health-check", methods=['GET'])
def users_health_check():
    return jsonify({"status": "OK"})


@app.route("/users", methods=['GET'])
def users_list():
    return jsonify(users)


@app.route("/users/<username>", methods=['GET'])
def user_record(username):
    if username not in users:
        raise NotFound

    return jsonify(users[username])


@app.route("/users/<username>/bookings", methods=['GET'])
def user_bookings(username):
    """
    Gets booking information from the 'Bookings Service' for the user, and
     movie ratings etc. from the 'Movie Service' and returns a list.
    :param username:
    :return: List of Users bookings
    """
    if username not in users:
        raise NotFound("User '{}' not found.".format(username))

    try:
        users_bookings = requests.get("http://{}:{}/bookings/{}".format(helper.resolve_requests_host(
            'bookings'), helper.get_port('bookings'), username), timeout=helper.get_timeout('bookings'))
    except requests.exceptions.ConnectionError:
        raise ServiceUnavailable("The Bookings service is unavailable.")
    except requests.exceptions.Timeout:
        raise ServiceUnavailable("The Bookings service timed out.")

    if users_bookings.status_code == 404:
        raise NotFound("No bookings were found for {}".format(username))

    if users_bookings.status_code != 200:
        raise ServiceUnavailable("The Bookings service is malfunctioning.")

    users_bookings = users_bookings.json()

    return jsonify(users_bookings)


@app.route("/users/<username>/suggested", methods=['GET'])
def user_suggested(username):
    """
    Returns movie suggestions. The algorithm returns a list of 3 top ranked
    movies that the user has not yet booked.
    :param username:
    :return: Suggested movies
    """
    raise NotImplementedError()


if __name__ == "__main__":
    app.run(port=helper.get_port('users'),
            host="0.0.0.0", debug=helper.get_debug())
