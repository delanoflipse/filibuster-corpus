
# Audio Assets (S3)

import helper
from flask import Flask, send_from_directory, jsonify
from werkzeug.exceptions import NotFound, Forbidden
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

with open("{}/audio-assets.json".format(parent_path), "r") as f:
    assets = json.load(f)


@app.route("/books/<book_id>/licenses/<license>", methods=['GET'])
def get_audio(book_id, license):
    if book_id not in assets:
        raise NotFound("book_id {} not found".format(book_id))
    if not check_license(license):
        raise Forbidden("license invalid")

    try:
        audio_path = assets[book_id]["audio"]
        return send_from_directory(parent_path, audio_path, as_attachment=True)
    except:
        raise NotFound("audio file not found")

# Dummy check


def check_license(license):
    return license != "invalid_license"


if __name__ == "__main__":
    app.run(port=helper.get_port('audio-assets'),
            host="0.0.0.0", debug=helper.get_debug())
