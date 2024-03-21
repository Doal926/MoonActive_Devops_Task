import requests
from flask import Flask

app = Flask(__name__)


@app.route("/metadata", methods=["GET"])
def get_metadata():
    token_resp = requests.put(
        "http://169.254.169.254/latest/api/token",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},
    )
    token = token_resp.text
    headers = {"X-aws-ec2-metadata-token": token}
    resp = requests.get("http://169.254.169.254/latest/meta-data", headers=headers)
    metadata = {}
    for key in resp.text.split("\n"):
        resp = requests.get(
            f"http://169.254.169.254/latest/meta-data/{key}", headers=headers
        )
        if resp.status_code != 200:
            print(resp.request)
        metadata[key] = resp.text
    return metadata


if __name__ == "__main__":
    app.run(host="0.0.0.0")
