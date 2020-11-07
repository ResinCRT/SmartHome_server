from mqtt.mqtt import MqttSub
from DBmanager import *
from utilsocket import DbSocket
from myparser import get_arguments
from decoder import *
import json
import time
from android_socket import AndroidSocket
import threading

def main():
    host, topic = get_arguments()
    server_port = 8888
    if host == None:  # set Default host IP and mqtt Topic
        host = "192.168.0.6"
        topic = "IoT3/home/#"

    print(host)
    print(topic)
    subscriber = MqttSub(host, topic)
    print(subscriber)

    test_db = MongoManager("localhost")
    test_db.connect_db()

    soc = DbSocket("", server_port)
    print(soc)
    # soc = AndroidSocket("", server_port)
    def store_DB(client, userdata, msg):
        message = msg.payload.json()

        dict_data = {"client": str(client),
                     "userdata": str(userdata),
                     "msg": message}
        cli = test_db.db_client['testDB']['test2']
        res = cli.insert_one(dict_data)
        lists = cli.find().sort("_id", -1).limit(1)
        print(f"message from topic[{subscriber.topic}]:{lists[0]['msg']}")

    def store_data(client, userdata, msg):
        datas = rf"{msg.payload.decode('utf-8')}"
        print(datas)
        try:
            json_data = json.loads(datas)
            soc.update_dict(msg)
            print(soc.dict_data)
        except json.JSONDecodeError:
            print("JSON decode fail : msg is not JSON")
        # subscriber.client.publish('IoT3/home/living/LED/info', r'send_to_LED', 1)

    def send_order(data):
        if not data:
            print("TCP socket disconnect")
            soc.set_flag(False)
            return
        # <<<<
        # decode ordermsg to target topic(dict)

        # <<<<
        try:
            print("message arriveed from socket")
            print(f"data:{data}")
            target_topic, msg = soc.handle_request(data)
            if target_topic != 'iot_app':
                subscriber.client.publish(target_topic, msg, 1)
            else:
                msg = msg.encode('utf-8')
                soc.client_sock.sendall(msg)
        except ValueError:
            print("[Error]: invalid Value")
            soc.set_flag(False)

    def publish_by_time(timer):
        def publishing():
            while True:
                subscriber.client.publish('iot_app', soc.getJson(), 1)
                time.sleep(timer)

        t = threading.Thread(target=publishing)
        t.setDaemon(True)
        t.start()

    def print_data(client, userdata, msg):
        print(str(msg.payload))
    soc.set_callback(send_order)
    subscriber.set_on_message(store_data)
    subscriber.connect_default()
    # mqtt client loops in another thread
    subscriber.run_loop()
    # socket open
    soc.run()
    publish_by_time(3)
    while True:
        print("main thread running")
        time.sleep(4)


if __name__ == "__main__":
    main()


