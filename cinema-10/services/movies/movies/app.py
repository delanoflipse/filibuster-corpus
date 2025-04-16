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
helper = helper.Helper("cinema-10")


with open("{}/cinema-10/services/movies/movies.json".format(examples_path), "r") as f:
    movies = json.load(f)


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
    if movieid not in movies:
        raise NotFound

    result = movies[movieid]
    result["uri"] = "/movies/{}".format(movieid)

    return jsonify(result)


@app.route("/movies", methods=['GET'])
def movie_record():
    return jsonify(movies)


if __name__ == "__main__":
    app.run(port=helper.get_port('movies'), host="0.0.0.0",
            debug=helper.get_debug(), threaded=True)
