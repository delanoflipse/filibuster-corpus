
# API Gateway

from flask import Flask, jsonify
from werkzeug.exceptions import NotFound, ServiceUnavailable, InternalServerError
import requests
import os, sys

app = Flask(__name__)

examples_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
sys.path.append(examples_path)
import helper 
helper = helper.Helper("expedia")



@app.route("/health-check", methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})

@app.route("/review/hotels/<hotel_id>", methods=['GET'])
def get_homepage(hotel_id):

    # Get ML sorted reviews
    result = None
    success = True
    try:
        reviews_response = requests.get("http://{}:{}/hotels/{}".format(helper.resolve_requests_host(
            'review-ml'), helper.get_port('review-ml'), hotel_id), timeout=helper.get_timeout('review-ml'))
        status_code = reviews_response.status_code
        if status_code == 404:
            raise NotFound("hotel_id {} not found".format(hotel_id))
        if status_code != 200:
            success = False
        else:
            result = reviews_response.json()
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        success = False

    if success:
        return jsonify(result)
            
    # Fallback to time sorted reviews
    try:
        reviews_response = requests.get("http://{}:{}/hotels/{}".format(helper.resolve_requests_host(
            'review-time'), helper.get_port('review-time'), hotel_id), timeout=helper.get_timeout('review-time'))
        status_code = reviews_response.status_code
        if status_code == 404:
            raise NotFound("hotel_id {} not found".format(hotel_id))
        if status_code != 200:
            raise ServiceUnavailable("Reviews are unavailable.")
        result = reviews_response.json()
    except requests.exceptions.ConnectionError:
        raise ServiceUnavailable("Fallback review service is unavailable.")
    except requests.exceptions.Timeout:
        raise ServiceUnavailable("Fallback review service timed out.")
            
    return jsonify(result)


if __name__ == "__main__":
    app.run(port=helper.get_port('api-gateway'), host="0.0.0.0", debug=helper.get_debug())
