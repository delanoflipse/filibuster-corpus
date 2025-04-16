
# Primary Database

from flask import Flask, Response, jsonify
from werkzeug.exceptions import Forbidden
import os, sys

app = Flask(__name__)

examples_path = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
sys.path.append(examples_path)
import helper
helper = helper.Helper("mailchimp")



@app.route("/health-check", methods=['GET'])
def db_primary_health_check():
    return jsonify({"status": "OK"})


@app.route("/read", methods=['GET'])
def read():
    return jsonify({"data": "dummy"})


READ_ONLY = os.getenv('DB_READ_ONLY') # "1" if DB is read only


@app.route("/write/urls/<url>", methods=['POST'])
def write(url):
    # In PHP (which, Mailchimp uses) the database error renders directly into the output.
    # So to simulate that we put something manually into the JSON when an error occurs.
    if READ_ONLY == "1":
        raise Forbidden("Database is read-only")

    return Response(status=200)


if __name__ == "__main__":
    app.run(port=helper.get_port('db-primary'), host="0.0.0.0", debug=helper.get_debug())
