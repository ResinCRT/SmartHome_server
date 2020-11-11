# conf를 읽어서
import json
import time
from src.util.decoder import msg_to_tuple




class Emergency:

    def __init__(self):
        self.timestamp = {}
        self.conf = None

    def init(self):
        self.conf = self.get_conf()

    def get_conf(self):
        # return array of emergency
        setting = {}
        try:
            with open('setting.conf') as f:
                setting = json.load(f)
        except FileNotFoundError:
            with open('setting.conf', 'w') as f:
                f.write('{}')
        except Exception as e:
            print(e)
        return setting

    def check_emergency(self, msg, client, conf=None):
        room, sensor, data = msg_to_tuple(msg)
        # if not conf:
        #     conf = get_conf()
        conf = self.conf
        if room in conf:
            if sensor in conf[room]:
                for opt, dat in data.items():
                    if opt in conf[room][sensor]:
                        comp = conf[room][sensor][opt]
                        # 상하 수치 체크
                        if ((comp[1] == "HIGH" and comp[0] < dat)
                         or (comp[1] == "LOW" and comp[0] > dat)):
                            client.publish(f'iot_app/emergency', f'{room}/{sensor}/{opt}/{comp[1]}', 2)

    def check_toilet(self, datas, client):
        PIR_state = False
        water_state = False

        if 'toilet' in datas:
            if 'pir_s' in datas['toilet']:
                PIR_state = bool(datas['toilet']['pir_s']['pir_s'])
            if 'wat_s' in datas['toilet']:
                water_state = bool(datas['toilet']['wat_s']['wat_s'])
            # print(f'PIR : {PIR_state} \nwater : {water_state}')
            if not PIR_state and water_state and 'toilet' not in self.timestamp:
                self.timestamp['toilet'] = [time.time(), 30]
                print('toilet count start')
            elif not PIR_state and water_state and 'toilet' in self.timestamp:
                if time.time() - self.timestamp['toilet'][0] >= self.timestamp['toilet'][1]:
                    print('30sec passed')
                    client.publish(f'iot_app/emergency', f'toilet/wat_s/flood', 2)
            elif not (not PIR_state and water_state) and 'toilet' in self.timestamp:
                self.timestamp.pop('toilet', None)
                client.publish(f'iot_app/emergency', f'toilet/wat_s/stop', 2)




if __name__ == "__main__":
    pass