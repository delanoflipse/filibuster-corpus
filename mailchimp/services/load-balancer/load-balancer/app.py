
# Load Balancer

import helper
from flask import Flask, jsonify
from werkzeug.exceptions import ServiceUnavailable, InternalServerError
import requests
import os
import sys

app = Flask(__name__)

examples_path = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
sys.path.append(examples_path)
helper = helper.Helper("mailchimp")


@app.route("/health-check", methods=['GET'])
def load_balancer_health_check():
    return jsonify({"status": "OK"})


@app.route("/urls/<url>", methods=['GET'])
def convert(url):
    try:
        app_server_response = requests.get("http://{}:{}/urls/{}".format(
            helper.resolve_requests_host('app-server'), helper.get_port('app-server'), url), timeout=helper.get_timeout('load-balancer'))
        if app_server_response.status_code == 500:
            return jsonify({"result": url})
        return jsonify(app_server_response.json())
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        raise ServiceUnavailable("The App Server is unavailable.")


if __name__ == "__main__":
    app.run(port=helper.get_port('load-balancer'),
            host='0.0.0.0', debug=helper.get_debug())
