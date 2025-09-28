from flask import Flask, jsonify
from werkzeug.exceptions import NotFound, ServiceUnavailable

import json
import os
import sys
import requests

app = Flask(__name__)

examples_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
sys.path.append(examples_path)
import helper 
helper = helper.Helper("cinema-3")


with open("{}/cinema-3/services/bookings/bookings.json".format(examples_path), "r") as f:
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
    return jsonify({ "status": "OK" })

@app.route("/bookings", methods=['GET'])
def booking_list():
    return jsonify(bookings)

@app.route("/bookings/<username>", methods=['GET'])
def booking_record(username):
    if username not in bookings:
        raise NotFound

    # For each booking, get the rating and the movie title
    result = {}
    for date, movies in bookings[username].items():
        result[date] = []
        for movieid in movies:
            try:
                movies_resp = requests.get("http://{}:{}/movies/{}".format(helper.resolve_requests_host('movies'), helper.get_port('movies'), movieid), timeout=helper.get_timeout('movies'))
            except requests.exceptions.ConnectionError:
                raise ServiceUnavailable("The Movie service is unavailable.")
            except requests.exceptions.Timeout:
                raise ServiceUnavailable("The Movie service timed out.")

            if movies_resp.status_code != 200:
                raise ServiceUnavailable("The Movie service is malfunctioning.")

            movies_resp = movies_resp.json()

            result[date].append({
                "title": movies_resp["title"],
                "rating": movies_resp["rating"],
                "uri": movies_resp["uri"]
            })

    return jsonify(result)

if __name__ == "__main__":
     app.run(port=helper.get_port('bookings'), host="0.0.0.0", debug=helper.get_debug())
