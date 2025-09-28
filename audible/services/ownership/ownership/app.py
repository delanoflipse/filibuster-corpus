
# Ownership service (DynamoDB)

from flask import Flask, Response, jsonify
import json
import os, sys
from werkzeug.exceptions import NotFound, Forbidden


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

with open("{}/ownership.json".format(parent_path), "r") as f:
    ownership = json.load(f)


@app.route("/users/<user_id>/books/<book_id>", methods=['GET'])
def check_auth(user_id, book_id):
    if user_id not in ownership:
        raise NotFound("user_id {} not found".format(user_id))
    elif book_id not in ownership[user_id]:
        raise Forbidden("user_id {} does not own book_id {}".format(user_id, book_id))
    
    return Response(status=200)


if __name__ == "__main__":
    app.run(port=helper.get_port('ownership'), host="0.0.0.0", debug=helper.get_debug())
