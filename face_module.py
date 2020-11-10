from face_recog_module import FaceRecog
from mqtt.mqtt import MqttNode

class FaceModule(FaceRecog):
    def __init__(self, host, topic):
        super().__init__()
        self.node = MqttNode(host)
        self.node.set_topic(topic)

    def recog_action(self, frame):
        self.node.client.publish(self.node.topic,r"Unknown Face recognized",1)

    def init(self):
        self.node.connect_default()
        self.node.run_loop()



if __name__ == "__main__":
    pass