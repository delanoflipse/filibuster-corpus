
# User Profile service
import helper
import time
import requests

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

with open("{}/users.json".format(parent_path), "r") as f:
    users = json.load(f)


@app.route("/users/<user_id>", methods=['GET'])
def get_profile(user_id):
    if not user_id in users:
        raise NotFound("user_id {} not found".format(user_id))

    # Record some telemetry.
    if os.environ.get('NETFLIX_FAULTS', ''):
        try:
            requests.post(helper.get_service_url("telemetry"),
                          json={"time": time.time()},
                          timeout=helper.get_timeout("telemetry"))

        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass

    return jsonify(users[user_id])


if __name__ == "__main__":
    app.run(port=helper.get_port("user-profile"),
            host="0.0.0.0", debug=helper.get_debug())
