
# User Recommendations service

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

with open("{}/user-recommendations.json".format(parent_path), "r") as f:
    user_recs = json.load(f)


@app.route("/users/<user_id>", methods=['GET'])
def get_user_recommendations(user_id):
    if not user_id in user_recs:
        raise NotFound("user_id {} not found".format(user_id))

    response = {}
    response["recommendations"] = user_recs[user_id]
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=helper.get_port("user-recommendations"),
            host="0.0.0.0", debug=helper.get_debug())
