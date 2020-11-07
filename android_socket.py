import socket
import time
import threading

class AndroidSocket:
    def __init__(self, host, port):
        self.host = host
        self.port = port  # Arbitrary non-privileged port
        self.client_sock = ''
        self.client_addr = ''
        self.callback = self.default_callback
        self.server_sock = None
        self.init()


    def init(self):
        self.server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(1)

    def run(self):
        while True:
            print("기다리는 중")
            self.client_sock, self.client_addr = self.server_sock.accept()

            print('Connected by', self.client_addr)
            data = self.client_sock.recv(1024).decode("utf-8")
            self.callback(data)
            self.client_sock.close()

    def default_callback(self, data):
        pass

    def set_callback(self, fun):
        self.callback = fun

    def terminate(self):
        self.client_sock.close()
        self.server_sock.close()


if __name__ == "__main__":
    sock = AndroidSocket("", 8888)
    sock.run()