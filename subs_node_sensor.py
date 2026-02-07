import json
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected to broker")
    client.subscribe("SmIr/nodesensor")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())

        # Kirim ke Laravel
        import requests
        res = requests.post("https://smartirrigation.nextiotlab.com/api/mqtt-receive", json=data)
        #res = requests.post("http://127.0.0.1:8000/api/mqtt-receive", json=data)
        print("Kirim ke Laravel:", res.status_code)

    except Exception as e:
        print("Error parsing JSON:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()
