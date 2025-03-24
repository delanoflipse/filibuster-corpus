
# Telemetry

import helper
from flask import Flask, request, Response, jsonify
from werkzeug.exceptions import InternalServerError
from threading import Thread, Lock

import json
import os
import sys
import random

app = Flask(__name__)

helper = helper.Helper("netflix")


@app.route("/health-check", methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})


parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_path)

file_path = "{}/logs.json".format(parent_path)


@app.route("/", methods=['POST'])
def record():
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                logs = json.load(f)
            if len(logs["logs"]) > 10:
                # truncate log
                logs["logs"] = []
            logs["logs"].append(request.json)
            with open(file_path, "w") as f:
                json.dump(logs, f)
        else:
            logs = {}
            logs["logs"] = []
            logs["logs"].append(request.json)
            with open(file_path, "w") as f:
                json.dump(logs, f)
    except:
        raise InternalServerError("Telemetry service error.")

    return Response(status=200)


if __name__ == "__main__":
    app.run(port=helper.get_port("telemetry"),
            host="0.0.0.0", debug=helper.get_debug())
