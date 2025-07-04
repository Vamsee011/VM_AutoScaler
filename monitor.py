from flask import Flask, jsonify
import psutil
import requests

app = Flask(__name__)

THRESHOLD = 20  # CPU usage threshold in percentage
HOST_IP = ""  # Host system IP
alert_sent = False

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

@app.route('/cpu', methods=['GET'])
def cpu_usage():
    global alert_sent
    cpu = get_cpu_usage()

    if cpu > THRESHOLD and not alert_sent:
        requests.get(f"http://{HOST_IP}:5001/scale")
        alert_sent = True

    return jsonify({"cpu_usage": cpu})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

