
# My List service

import helper
from flask import Flask, jsonify
from werkzeug.exceptions import NotFound

import json
import os
import sys

app = Flask(__name__)

helper = helper.Helper("netflix")


@app.route("/health-check", methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})


parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_path)

with open("{}/movie_list.json".format(parent_path), "r") as f:
    movie_list = json.load(f)


@app.route("/users/<user_id>", methods=['GET'])
def get_my_list(user_id):
    if not user_id in movie_list:
        raise NotFound("user_id {} not found".format(user_id))
    response = {}
    response["my-list"] = movie_list[user_id]
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=helper.get_port("my-list"),
            host="0.0.0.0", debug=helper.get_debug())
