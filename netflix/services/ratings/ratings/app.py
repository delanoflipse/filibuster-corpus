
# Ratings service

from flask import Flask, jsonify
from werkzeug.exceptions import NotFound

import json
import os
import sys

app = Flask(__name__)

examples_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
sys.path.append(examples_path)
import helper 
helper = helper.Helper("netflix")



@app.route("/health-check", methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})

parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_path)

with open("{}/ratings.json".format(parent_path), "r") as f:
    ratings = json.load(f)

@app.route("/users/<user_id>", methods=['GET'])
def get_ratings(user_id):
    if not user_id in ratings:
        raise NotFound("user_id {} not found".format(user_id))

    response = {}
    response["ratings"] = ratings[user_id]
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=helper.get_port("ratings"), host="0.0.0.0", debug=helper.get_debug())