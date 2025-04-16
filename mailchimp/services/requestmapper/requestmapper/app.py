
# Requestmapper

from flask import Flask, jsonify
import os, sys

examples_path = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))))))
sys.path.append(examples_path)
import helper
helper = helper.Helper("mailchimp")

app = Flask(__name__)

@app.route("/health-check", methods=['GET'])
def requestmapper_health_check():
    return jsonify({ "status": "OK" })


@app.route("/urls/<url>", methods=['GET'])
def get_url(url):
    if url == "prettyurl":
        return jsonify({"result": "internalurl"})
    return jsonify({"result": url})


if __name__ == "__main__":
    app.run(port=helper.get_port('requestmapper'), host='0.0.0.0', debug=helper.get_debug())
