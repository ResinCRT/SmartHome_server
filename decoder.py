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
                    topic += f'/{req[1]}'
                    msg = rf'{req[1]}_{req[2]}'
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
    return topic[-3], topic[-2], data_dict


