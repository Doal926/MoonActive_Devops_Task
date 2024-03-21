import requests
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/metadata", methods=["GET"])
def get_metadata():
    # Get the token
    token_resp = requests.put(
        "http://169.254.169.254/latest/api/token",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
    )
    token = token_resp.text
    headers = {"X-aws-ec2-metadata-token": token}

    # Get the metadata
    resp = requests.get("http://169.254.169.254/latest/meta-data", headers=headers)
    return jsonify({"metadata": resp.text})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
