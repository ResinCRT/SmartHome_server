from src.util.mqtt import MqttSub
from src.util.DBmanager import *
from src.net_server.utilsocket import DbSocket, FileSocket
from src.util.myparser import get_arguments
from src.net_server.emergency import *
import json
import time
import threading

def mqtt_main():
    host, topic = get_arguments()
    server_port = 8888
    file_port = 8890
    if host == None:  # set Default host IP and mqtt Topic
        host = "192.168.0.138"
        topic = "iot3/+/+/"
    emerg = Emergency()
    emerg.init()
    print(emerg.conf)

    print(host)
    print(topic)
    subscriber = MqttSub(host, topic)
    print(subscriber)

    # test_db = MongoManager("localhost")
    # test_db.connect_db()

    filesoc = FileSocket("", file_port)
    soc = DbSocket("", server_port)
    print(soc)
    print(filesoc)
    # soc = AndroidSocket("", server_port)


    # def store_DB(client, userdata, msg):
    #     message = msg.payload.json()
    #
    #     dict_data = {"client": str(client),
    #                  "userdata": str(userdata),
    #                  "msg": message}
    #     cli = test_db.db_client['testDB']['test2']
    #     res = cli.insert_one(dict_data)
    #     lists = cli.find().sort("_id", -1).limit(1)
    #     print(f"message from topic[{subscriber.topic}]:{lists[0]['msg']}")


    def store_data(client, userdata, msg):
        datas = rf"{msg.payload.decode('utf-8')}"
        print("message:", datas)
        try:
            # json_data = json.loads(datas)
            soc.update_dict(msg)
            emerg.check_emergency(msg, subscriber.client)
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
            print("message arrived from socket")
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
                emerg.check_toilet(soc.dict_data, subscriber.client)

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
    filesoc.set_file('test.txt')
    filesoc.set_path('static/knowns')
    filesoc.run()
    publish_by_time(3)
    print("main thread running")
    while True:
        # main task
        time.sleep(4)


if __name__ == "__main__":
    mqtt_main()


