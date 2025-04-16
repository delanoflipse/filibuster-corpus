
# Review service sorted by time

from flask import Flask, jsonify
from werkzeug.exceptions import NotFound

import json
import os
import sys

app = Flask(__name__)

examples_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
sys.path.append(examples_path)
import helper 
helper = helper.Helper("expedia")


parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_path)

with open("{}/reviews.json".format(parent_path), "r") as f:
    reviews = json.load(f)


@app.route("/health-check", methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})

@app.route("/hotels/<hotel_id>", methods=['GET'])
def get_reviews(hotel_id):
    if not hotel_id in reviews:
        raise NotFound("hotel_id {} not found".format(hotel_id))

    response = {}
    response["reviews"] = reviews[hotel_id]
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=helper.get_port('review-time'), host="0.0.0.0", debug=helper.get_debug())
