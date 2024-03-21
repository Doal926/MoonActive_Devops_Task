from flask import Flask
import requests

app = Flask(__name__)

@app.route('/metadata', methods=['GET'])
def get_metadata():
    response = requests.put("http://169.254.169.254/latest/api/token", headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"})
    print(response)
    token = response.text

    headers = {"X-aws-ec2-metadata-token": token}
    response = requests.get("http://169.254.169.254/latest/meta-data/instance-id", headers=headers)
    instance_id = response.text
    print(instance_id)
    return f"\n{instance_id}\n\n"
if __name__ == '__main__':
    app.run()