# conf를 읽어서
import json
from src.util.decoder import msg_to_tuple


def get_conf():
    # return array of emergency
    setting = {}
    with open('setting.conf') as f:
        try:
            setting = json.load(f)
        except Exception as e:
            print(e)
    return setting


def check_emergency(msg, client, conf=None):
    room, sensor, data = msg_to_tuple(msg)
    if not conf:
        conf = get_conf()

    if room in conf:
        if sensor in conf[room]:
            for opt, dat in data.items():
                if opt in conf[room][sensor]:
                    comp = conf[room][sensor][opt]
                    if ((comp[1] == "HIGH" and comp[0] < dat)
                     or (comp[1] == "LOW" and comp[0] > dat)):
                        client.publish(f'iot_app/emergency', f'{room}/{sensor}/{opt}/{comp[1]}', 2)


if __name__ == "__main__":
    get_conf()