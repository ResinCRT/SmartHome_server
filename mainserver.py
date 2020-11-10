import multiprocessing as mp
from Fserver import stream_main
from server import mqtt_main
import sys

if __name__ == '__main__':
    mp.set_start_method('spawn')
    mqtt_server = mp.Process(target=mqtt_main, daemon=True)
    stream_server = mp.Process(target=stream_main, daemon=True)

    mqtt_server.start()
    stream_server.start()
    mqtt_server.join()
    stream_server.join()

