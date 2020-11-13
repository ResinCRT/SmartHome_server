import paho.mqtt.client as mqtt
import time
import json
import threading
class MqttNode:
    def __init__(self, server):
        self.client = mqtt.Client()
        self.server = server
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.topic = "test"

    def __str__(self):
        return f"<MqttNode client:{self.client} server:{self.server} topic:{self.topic}"

    def on_connect(self, client, userdata, flags, rc):
        print("connected with code :" + str(rc))
        self.client.subscribe(self.topic)

    def set_topic(self, topic):
        self.topic = topic

    def on_message(self, client, userdata, msg):
        print(str(msg.payload))

    def set_on_publish(self, fun):
        self.client.on_publish = fun

    def set_on_connect(self, fun):
        self.client.on_connect = fun

    def set_on_message(self,fun):
        self.client.on_message = fun

    def connect_default(self):
        self.client.connect(self.server, 1883, 60)

    def run_loop(self):
        self.client.loop_start()

    def run_forever(self):
        self.client.loop_forever()

    def send_multiple_message(self, dict_data):
        for key, value in dict_data.items():
            self.client.publish(key, rf'{value}', qos=1)


class MqttSub(MqttNode):

    def __init__(self, server, topic):
        super().__init__(server)
        self.set_topic(topic)

    def connect_default(self):
        self.client.connect(self.server, 1883)


class MqttPub(MqttNode):
    def __init__(self, server):
        super().__init__(server)

    def __str__(self):
        super().__str__()

    def connect_default(self):
        self.client.connect(self.server, 1883)


if __name__ == "__main__":
    subscriber = MqttSub("192.168.0.20")
    print(subscriber)
    subscriber.set_topic("mqtttest2")
    subscriber.connect_default()
    subscriber.run_forever()

    # client = mqtt.Client()
    # def on_connect(client, userdata, flags, rc):
    #     print("connected with code :" + str(rc))
    #     client.subscribe("mqtttest")
    #
    # def on_message(self, client, userdata, msg):
    #     print(str(msg.payload))
    # client.on_connect = on_connect
    # client.on_message = on_message
    # client.connect("192.168.0.20")
    # client.loop_start()

    #subscriber.run()



