import paho.mqtt.client as mqtt
import requests

# MQTT config
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "test/sayyid"

# Laravel API URL (ganti sesuai IP atau domain server kamu)
LARAVEL_API_URL = "http://127.0.0.1:8000/api/mqtt-receive"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with code:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received from [{msg.topic}]: {message}")

    # Kirim ke Laravel API
    try:
        response = requests.post(LARAVEL_API_URL, json={
            'topic': msg.topic,
            'message': message
        })
        print(f"Sent to Laravel: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Error: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
