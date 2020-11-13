from src.stream_server.face_recog_module import FaceRecog
from src.util.mqtt import MqttNode
import cv2
import socket
from _thread import start_new_thread
from src.util.android_socket import AndroidSocket


class FaceModule(FaceRecog):
    def __init__(self, host, topic, path, cam):
        super().__init__(path, cam)
        self.node = MqttNode(host)
        self.node.set_topic(topic)
        self.shot = None

    def send_socket_msg(self):
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            addr = '127.0.0.1'
            port = 8888
            soc.connect((addr, port))
            msg = f'living_door_0'.encode('utf-8')
            soc.send(msg)
            soc.close()
        except Exception as e:
            print('[Error]:', e)

    def recog_action(self, frame, dist):
        for face in self.known_face_names:
            if face in self.face_names:
                temp = 'iot3/door/door/info'
                print(f'face:{face} distance: {dist:.2f}')
                # self.node.client.publish(self.node.topic, rf"Face recognized: {face}", qos=1)
                start_new_thread(self.send_socket_msg)
                # self.node.client.publish(temp, r"255", 2)


    def unknown_action(self, frame):
        self.node.client.publish(self.node.topic, r"Unknown Face recognized", qos=1)
        self.node.client.loop_stop()
        _, jpg = cv2.imencode('.jpg', frame)
        self.shot = jpg.tobytes()

    def init(self):
        self.node.connect_default()
        self.node.run_loop()


if __name__ == "__main__":
    pass
