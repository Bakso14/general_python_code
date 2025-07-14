import requests

API_URL = "http://127.0.0.1:8000/api/sensor/store"
payload = {
    "node_id": "Node 1",
    "suhu": 30.0,
    "kelembaban": 60.2,
    "gas": 300
}

try:
    response = requests.post(API_URL, json=payload)
    print("✅ Status:", response.status_code)
    print("🔁 Respons:", response.text)
except Exception as e:
    print("❌ Error:", e)
