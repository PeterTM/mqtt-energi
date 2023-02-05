from paho.mqtt import client as mqtt_client

client_id = f'myenergy-mqtt-1'

def connect(broker,port):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    mqtt = mqtt_client.Client(client_id)
    mqtt.on_connect = on_connect
    mqtt.connect(broker, port)
    return mqtt
