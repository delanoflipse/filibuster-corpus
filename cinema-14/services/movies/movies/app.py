import helper
import queue
import time

from flask import Flask, jsonify
from werkzeug.exceptions import NotFound, TooManyRequests

import json
import os
import sys

app = Flask(__name__)

examples_path = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
sys.path.append(examples_path)
helper = helper.Helper("cinema-14")


with open("{}/cinema-14/services/movies/movies.json".format(examples_path), "r") as f:
    movies = json.load(f)

q = queue.Queue()
MAX_QUEUE_SIZE = 5


@app.route("/", methods=['GET'])
def hello():
    return jsonify({
        "uri": "/",
        "subresource_uris": {
            "movies": "/movies",
            "movie": "/movies/<id>"
        }
    })


@app.route("/health-check", methods=['GET'])
def movies_health_check():
    return jsonify({"status": "OK"})


@app.route("/movies/<movieid>", methods=['GET'])
def movie_info(movieid):
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

    if movieid not in movies:
        raise NotFound

    result = movies[movieid]
    result["uri"] = "/movies/{}".format(movieid)

    return jsonify(result)


@app.route("/movies", methods=['GET'])
def movie_record():
    return jsonify(movies)


if __name__ == "__main__":
    app.run(port=helper.get_port('movies'),
            host="0.0.0.0", debug=helper.get_debug())
