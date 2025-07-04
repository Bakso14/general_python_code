
from playsound import playsound
import random
from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"

topic_tandon = "rumah/sensortandon";
topic_arus = "rumah/sensorarus";
topic_tegangan = "rumah/sensortegangan";

# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1,client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        # print(type(msg.payload.decode()))
        
        if(msg.topic == topic_tandon):
            if(msg.payload.decode() == '11'):
                print("PENUH")
                playsound('F:/Github/general_python_code/sound/suara_cek.mp3')
            elif(msg.payload.decode() == '01'):
                print("BERKURANG")
            elif(msg.payload.decode() == '00'):
                print("KOSONG")
                playsound('F:/Github/general_python_code/sound/suara_cek.mp3')
                

    client.subscribe(topic_tandon)
    client.subscribe(topic_arus)
    client.subscribe(topic_tegangan)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
