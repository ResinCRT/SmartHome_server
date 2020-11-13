from src.util.android_socket import AndroidSocket
from src.util.decoder import *
import threading
from _thread import start_new_thread
import json


class DbSocket(AndroidSocket):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.dict_data = {}
        self.flag = True
        self.conf = None
        self.sync_data = {}

    def synchronize(self):
        message = {}
        for key, value in self.sync_data.items():
            room, sensor = decode_topic(key)
            if room in self.dict_data:
                if sensor in self.dict_data[room]:
                    if type(self.dict_data[room][sensor]) == dict:
                        _, d_value = list(self.dict_data[room][sensor].items())[0]
                        if int(d_value) != int(value):
                            message[key] = int(value)
                else:
                    message[key] = int(value)
            else:
                message[key] = int(value)
        return message

    def update_dict(self, msg):
        room, sensor, data = msg_to_tuple(msg)
        if type(room) != str:
            print("unknown data format:", data)
        else:
            if room not in self.dict_data:
                self.dict_data[room] = {}
            self.dict_data[room][sensor] = data

    def update_sync(self, topic, msg):
        self.sync_data[topic] = msg

    def getJson(self, file=None):
        if type(self.dict_data) == dict:
            if file:
                return json.dump(self.dict_data, file, indent=4)
            else:
                return json.dumps(self.dict_data)

    def handle_request(self, data):
        target_topic, msg = decoder_test(data)
        if type(msg) == str:
            self.update_sync(target_topic, msg)
            return target_topic, msg
        elif type(msg) == list:
            target = msg[1]
            if target == 'ALL':
                dict_before_json = json.dumps(self.dict_data)
            else:
                try:
                    dict_before_json = {f"{target}": self.dict_data[f'{target}']}
                    result = json.dumps(dict_before_json)
                except KeyError:
                    dict_before_json = {"Error": "Invalid Key" }

            return target_topic, result

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


class FileSocket(AndroidSocket):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.path = ''
        self.file_name = ''

    def set_path(self, path):
        self.path = path

    def set_file(self, name):
        self.file_name = name

    def receive_thread(self, client_socket, addr):
        try:
            # 파일 크기 수신
            datas = client_socket.recv(1024)

            name, size = datas.decode('utf-8').split()
            self.set_file(name + '.jpg')
            size = int(size)

            print("수신할 파일 크기:", size)
            print("수신할 파일 이름:", self.file_name)

            # 준비상태 전송
            client_socket.send("ready".encode())

            # 파일 수신

            total_size = 0
            file_string = self.path + '/' + self.file_name
            with open(file_string, "wb") as f:
                while True:
                    data = client_socket.recv(1024)
                    f.write(data)
                    total_size += len(data)
                    if total_size >= size:
                        break
                print(f"수신 완료: {total_size} bytes")

        except Exception as e:
            print(e)

        finally:
            client_socket.close()

    def run(self):
        def runth():
            while True:
                print("socket 연결 기다리는 중")
                self.client_sock, self.client_addr = self.server_sock.accept()
                print('Connected by', self.client_addr)

                start_new_thread(self.receive_thread, (self.client_sock, self.client_addr))

        t = threading.Thread(target=runth)
        t.setDaemon(True)
        t.start()
        return t





