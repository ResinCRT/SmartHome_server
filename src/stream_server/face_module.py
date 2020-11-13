from src.stream_server.face_recog_module import FaceRecog
from src.util.mqtt import MqttNode
import cv2

class FaceModule(FaceRecog):
    def __init__(self, host, topic, path, cam):
        super().__init__(path, cam)
        self.node = MqttNode(host)
        self.node.set_topic(topic)
        self.shot = None

    def recog_action(self, frame, dist):
        for face in self.known_face_names:
            if face in self.face_names:
                temp = 'iot3/door/door/info'
                print(f'face:{face} distance: {dist:.2f}')
                self.node.client.publish(self.node.topic, rf"Face recognized: {face}", qos=1)
                self.node.client.publish(temp, r"255", 2)
                self.node.client.loop_stop()

    def unknown_action(self, frame):
        self.node.client.publish(self.node.topic + '/unknown', r"Unknown Face recognized", qos=1)
        _, jpg = cv2.imencode('.jpg', frame)
        self.shot = jpg.tobytes()

    def init(self):
        self.node.connect_default()
        self.node.run_loop()


if __name__ == "__main__":
    pass
