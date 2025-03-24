
# mobile client

import helper
from flask import Flask, jsonify
from werkzeug.exceptions import NotFound, ServiceUnavailable, InternalServerError

import os
import sys
import requests

app = Flask(__name__)

helper = helper.Helper("netflix")


@app.route("/health-check", methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})


parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_path)


@app.route("/netflix/homepage/users/<user_id>", methods=['GET'])
def get_netflix_homepage(user_id):
    try:
        api_gateway_response = requests.get("{}/homepage/users/{}".format(
            helper.get_service_url('api-gateway'), user_id), timeout=helper.get_timeout('api-gateway'))
        status_code = api_gateway_response.status_code

    except requests.exceptions.ConnectionError:
        raise ServiceUnavailable("The API Gateway is unavailable.")
    except requests.exceptions.Timeout:
        raise ServiceUnavailable("The API Gateway timed out.")

    if status_code == 404:
        raise NotFound("user_id {} not found".format(user_id))
    if status_code == 503:
        raise ServiceUnavailable()
    if status_code == 500:
        raise ServiceUnavailable("netflix is unavailable.")

    res = api_gateway_response.json()
    return jsonify(res)


if __name__ == "__main__":
    app.run(port=helper.get_port('mobile-client'),
            host="0.0.0.0", debug=helper.get_debug())
