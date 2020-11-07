import multiprocessing as mp
from Fserver import stream_main
from server import main
import sys

if __name__ == '__main__':
    mp.set_start_method('spawn')
    mqtt_server = mp.Process(target=main, daemon=True)
    stream_server = mp.Process(target=stream_main, daemon=True)
    print('start')
    mqtt_server.start()
    stream_server.start()
    mqtt_server.join()
    stream_server.join()

