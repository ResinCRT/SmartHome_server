from flask import Flask
from flask import render_template
from flask import Response
from src.util.USBcam import *
from src.stream_server.face_module import FaceModule
from src.util.myparser import get_arguments

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_fed')
def video_fed():
    camera = USBCam(show=True)
    return Response(camera.run(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed')
def video_feed():
    host, _ = flask_arguments()
    rec = FaceModule(host, 'iot_app/unknown', 'static/knowns')
    rec.init()
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

def flask_arguments():
    host, _ = get_arguments()
    topic = 'iot_app'
    if not host:
        host = '192.168.0.6'
    return host, topic

def stream_main():
    host, _ = flask_arguments()
    app.run(host=host, port=7072, debug=False)


if __name__ == '__main__':
    stream_main()