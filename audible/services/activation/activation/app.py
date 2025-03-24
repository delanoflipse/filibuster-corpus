
# Activation service (EC2)

import helper
from flask import Flask, jsonify
from werkzeug.exceptions import NotFound

import json
import os
import sys

app = Flask(__name__)

helper = helper.Helper("audible")


@app.route("/health-check", methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})


parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_path)

with open("{}/activation.json".format(parent_path), "r") as f:
    books = json.load(f)


@app.route("/books/<book_id>", methods=['GET'])
def get_license(book_id):
    response = {}
    if not book_id in books:
        raise NotFound("book_id {} not found".format(book_id))

    response["license"] = books[book_id]
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=helper.get_port('activation'),
            host="0.0.0.0", debug=helper.get_debug())
