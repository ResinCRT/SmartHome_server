from flask import Flask
from flask import render_template
from flask import Response
from src.util.USBcam import *
from src.stream_server.face_module import FaceModule
from src.util.myparser import get_arguments


class MainModule:
    def __init__(self):
        self.camera = None
        self.host, self.topic = None, None
        self.face = None

    def init(self):
        self.camera = USBCam(show=True)
        print('main camera init')
        self.host, self.topic = flask_arguments()
        self.face = FaceModule(self.host, 'iot_app/unknown', 'static/knowns', self.camera)
        self.face.init()


def flask_arguments():
    host, _ = get_arguments()
    topic = 'iot_app'
    if not host:
        host = '192.168.0.6'
    return host, topic


app = Flask(__name__)
server_module = MainModule()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_fed')
def video_fed():
    # camera = USBCam(show=True)
    rec = server_module.face
    return Response(rec.shot, mimetype='image/jpeg')


@app.route('/video_feed')
def video_feed():
    # host, _ = flask_arguments()
    # rec = FaceModule(host, 'iot_app/unknown', 'static/knowns')
    # rec.init()
    rec = server_module.face
    return Response(rec.run(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_snap')
def video_snap():
    camera = USBCam(show=True)
    return Response(camera.snapshot(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/shot')
def shot():
    return render_template('snap.html')


def gen(fr):
    while True:
        jpg_bytes = fr.get_jpg_bytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpg_bytes + b'\r\n\r\n')


def stream_main():
    host, _ = flask_arguments()

    server_module.init()
    app.run(host=host, port=7072, debug=False)


if __name__ == '__main__':
    stream_main()
