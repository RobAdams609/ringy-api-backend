from flask import Flask, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

CALL_API_KEY = os.environ.get("CALL_API_KEY")
LEAD_API_KEY = os.environ.get("LEAD_API_KEY")
CALL_API_URL = "https://app.ringy.com/api/public/external/get-calls"
LEAD_API_URL = "https://app.ringy.com/api/public/external/get-lead"

AGENTS = {
    "agent_rob": "Rob",
    "agent_fabricio": "Fabricio",
    "agent_phil": "Phil"
}

CALL_IDS = ["c15e46fe-4721-4d1c-abbd-ba857cf967d5"]
LEAD_IDS = ["f60e9415-b25c-4634-8e10-b72d37ed5b50"]

def fetch_call_data():
    data = []
    for call_id in CALL_IDS:
        r = requests.post(CALL_API_URL, json={"apiKey": CALL_API_KEY, "callId": call_id})
        if r.status_code == 200:
            data.append(r.json())
    return data

def fetch_lead_data():
    data = []
    for lead_id in LEAD_IDS:
        r = requests.post(LEAD_API_URL, json={"apiKey": LEAD_API_KEY, "leadId": lead_id})
        if r.status_code == 200:
            data.append(r.json())
    return data

@app.route("/metrics.json")
def metrics():
    today = datetime.utcnow().date()
    sample_stats = {
        "Rob": {"calls": 20, "sales": 2, "av": 8400, "talk": 85},
        "Fabricio": {"calls": 130, "sales": 9, "av": 37800, "talk": 540},
        "Phil": {"calls": 130, "sales": 9, "av": 37800, "talk": 540}
    }
    response = {
        "today": sample_stats,
        "week": sample_stats,
        "month": sample_stats
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
