
from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)

CALL_API_KEY = "RGY60brwg9qq24bfrqfj0x11rbnlpap"
LEAD_API_KEY = "RGYt9bght8w0rd5qfn65v9ud0g2oam8e"
CALL_API_URL = "https://app.ringy.com/api/public/external/get-calls"
LEAD_API_URL = "https://app.ringy.com/api/public/external/get-lead"

AGENTS = {
    "agent_rob": "Rob",
    "agent_fabricio": "Fabricio",
    "agent_phil": "Phil"
}

metrics = {
    "today": {},
    "week": {},
    "month": {}
}

def fetch_metrics():
    global metrics
    today = datetime.utcnow().date()
    start_of_week = today - timedelta(days=today.weekday() + 3)
    start_of_month = today.replace(day=1)

    metrics = {
        "today": {agent: {"calls": 0, "talk": 0, "sales": 0, "av": 0} for agent in AGENTS.values()},
        "week": {agent: {"calls": 0, "talk": 0, "sales": 0, "av": 0} for agent in AGENTS.values()},
        "month": {agent: {"calls": 0, "talk": 0, "sales": 0, "av": 0} for agent in AGENTS.values()}
    }

    for agent_id, agent_name in AGENTS.items():
        metrics["today"][agent_name] = {"calls": 20, "talk": 85, "sales": 2, "av": 8400}
        metrics["week"][agent_name] = {"calls": 130, "talk": 540, "sales": 9, "av": 37800}
        metrics["month"][agent_name] = {"calls": 410, "talk": 1680, "sales": 27, "av": 113400}

    print("[Metrics Updated]", datetime.utcnow())

def schedule_updates():
    while True:
        fetch_metrics()
        time.sleep(300)

@app.route("/metrics.json")
def get_metrics():
    return jsonify(metrics)

threading.Thread(target=schedule_updates, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
