from paho.mqtt import client as mqtt_client

def connect(broker,port, id):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    mqtt = mqtt_client.Client(id)
    mqtt.on_connect = on_connect
    mqtt.connect(broker, port)
    return mqtt
