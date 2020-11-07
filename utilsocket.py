from android_socket import AndroidSocket
from decoder import msg_to_tuple, decoder_test
import threading
import json


class DbSocket(AndroidSocket):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.dict_data = {}
        self.flag = True

    def update_dict(self, msg):
        room, sensor, data = msg_to_tuple(msg)
        if room not in self.dict_data:
            self.dict_data[room] = {}
        self.dict_data[room][sensor] = data

    def getJson(self):
        if type(self.dict_data) == dict:
            return json.dumps(self.dict_data)



    def handle_request(self, data):
        target_topic, msg = decoder_test(data)
        if type(msg) == str:
            return target_topic, msg
        elif type(msg) == list:
            target = msg[1]
            if target == 'ALL':
                dict_before_json = json.dumps(self.dict_data)
            else:
                try:
                    dict_before_json = {f"{target}": self.dict_data[f'{target}']}
                    output = json.dumps(dict_before_json)
                except KeyError:
                    dict_before_json = {"Error": "Invalid Key" }

            return target_topic, output



    def set_flag(self, boolOP):
        self.flag = boolOP

    def terminate(self):
        self.flag = False

    def run(self):
        self.set_flag(True)

        def runth():
            while self.flag:
                print("socket 연결 기다리는 중")
                self.client_sock, self.client_addr = self.server_sock.accept()
                print('Connected by', self.client_addr)
                data = self.client_sock.recv(1024).decode("utf-8")
                self.callback(data)
                self.client_sock.close()
        t = threading.Thread(target=runth)
        t.setDaemon(True)
        t.start()
        return t




