
# Content Delivery Engine (EC2)

import helper
from flask import Flask, jsonify
import os
import sys
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)
helper = helper.Helper("audible")


@app.route("/health-check", methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})


parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_path)

with open("{}/cache.json".format(parent_path), "r") as f:
    cache = json.load(f)


# Retrieve static metadata (e.g. asset locations)
# for requested audiobook
# Return url to user so that user can reach content delivery service
@app.route("/users/<user_id>/books/<book_id>", methods=['GET'])
def resolve_url(user_id, book_id):
    response = {}
    if book_id not in cache:
        raise NotFound("book_id {} not found".format(book_id))
    response["url"] = helper.get_service_url(
        "content-delivery-service") + "/users/{}/books/{}".format(user_id, book_id)
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=helper.get_port('content-delivery-engine'),
            host="0.0.0.0", debug=helper.get_debug())
