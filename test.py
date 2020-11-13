# import cv2
#
# image = cv2.imread("static/knowns/Sehoon.jpg", cv2.IMREAD_COLOR)
# resized = cv2.resize(image, (480, 640), interpolation=cv2.INTER_AREA )
# cv2.imwrite('SehoonR.jpg', resized)


from src.util.mqtt import MqttNode
import time
import json


data = {'test': 0, 'test2': 1}
key, value = list(data.items())[0]
print(data.items())
print(key, ':', value)
if __name__ == "dfd":
    host = '192.168.0.138'
    port = 1883
    soc = MqttNode(host)
    soc.set_topic('#')
    soc.connect_default()
    while True:
        ins = input(">>")
        PIR = {}
        waterSensor = {}
        waterSensor['wat_s'] = int(ins.split()[1])
        PIR['pir_s'] = int(ins.split()[0])
        out_P = json.dumps(PIR)
        out_w = json.dumps(waterSensor)
        soc.client.publish('iot3/toilet/pir_s', out_P, 1)
        time.sleep(1)
        soc.client.publish('iot3/toilet/wat_s', out_w, 1)
    # datas = {}
    # datas['Humi'] = 10
    # datas['Temp'] = 35
    # datas2 = {}
    # datas2['Brig'] = 255
    # datas2['Stat'] = 1
    # datas3 = {}
    # datas3['Win'] = 5
    # while True:
    #     out = json.dumps(datas)
    #     datas['Temp'] += 1
    #     datas['Humi'] += 1
    #     soc.client.publish('iot3/living/DHT', out, 1)
    #     print('data1')
    #     time.sleep(2)
    #     out2 = json.dumps(datas2)
    #     datas2['Brig'] += 1
    #     datas2['Stat'] *= -1
    #     soc.client.publish('iot3/inner/LED', out2, 1)
    #     print('data2')
    #     time.sleep(2)
    #     out3 = json.dumps(datas3)
    #     datas3['Win'] += 1
    #     soc.client.publish('iot3/living/window', out3, 1)
    #     print('data3')
    #     time.sleep(2)