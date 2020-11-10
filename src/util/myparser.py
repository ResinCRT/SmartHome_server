import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(nargs='*', help='Example)python test.py 192.168.0.1 testTopic', dest='args')
    if len(parser.parse_args().args) < 2:
        return None, None
    host = parser.parse_args().args[0]
    topic = parser.parse_args().args[1]

    return host, topic