
# Stats service (Amazon RDS)

from flask import Flask, Response, jsonify
from werkzeug.exceptions import InternalServerError
import json
import os, sys

app = Flask(__name__)

examples_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
sys.path.append(examples_path)
import helper 
helper = helper.Helper("audible")


@app.route("/health-check", methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})

parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_path)

file_path = "{}/stats.json".format(parent_path)

@app.route("/users/<user_id>/books/<book_id>", methods=['POST'])
def record(user_id, book_id):
    # Record user activity
    try:
        # Append to existing log and truncate if the log is too long.
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                stats = json.load(f)
            if len(stats["logs"]) > 10:
                # truncate log
                stats["logs"] = []
            stats["logs"].append({'user_id': user_id, 'book_id': book_id})
            with open(file_path, "w") as f:
                json.dump(stats, f)
        # File doesn't exist, therefore we have to create it.
        else:
            stats = {}
            stats["logs"] = []
            stats["logs"].append({'user_id': user_id, 'book_id': book_id})
            with open(file_path, "w") as f:
                json.dump(stats, f)
    except:
        raise InternalServerError("Stats service error.")

    return Response(status=201)

if __name__ == "__main__":
    app.run(port=helper.get_port('stats'), host="0.0.0.0", debug=helper.get_debug())