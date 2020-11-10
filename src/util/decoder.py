import json


def decoder_test(req):
    #topic = 'IoT3/home'
    topic = ''
    msg = ''
    try:
        if type(req) is str:
            req = req.split('_')
            if len(req) > 1:
                if req[0] == 'GET':
                    topic = 'iot_app'
                    msg = req
                elif len(req) >= 3:
                    topic += f'{req[0]}'
                    topic += f'/{req[1]}/info'
                    temp = req[2]
                    if req[2] == 'ON':
                        temp = 255
                    elif req[2] == 'OFF':
                        temp = 0
                    msg = rf'{temp}'
    except IndexError:
        print("Unavailable Request")
    print(topic)
    print(msg)
    return topic, msg


def msg_to_tuple(msg):
    data = rf"{msg.payload.decode('utf-8')}"
    data_dict = json.loads(data)
    output = {}
    topic = msg.topic.split('/')
    try:
        return topic[-2], topic[-1], data_dict
    except Exception as e:
        print(e)



