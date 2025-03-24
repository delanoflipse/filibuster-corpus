
# Global Recommendations service

import helper
from flask import Flask, jsonify

import os
import sys

app = Flask(__name__)

helper = helper.Helper("netflix")


@app.route("/health-check", methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})


parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_path)


@app.route("/", methods=['GET'])
def get_global_recommendations():
    response = {
        "recommendations": ["Inception", "Shutter Island", "The Dark Night"]
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=helper.get_port("global-recommendations"),
            host="0.0.0.0", debug=helper.get_debug())
