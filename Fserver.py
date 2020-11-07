from flask import Flask
from flask import render_template
from flask import Response
from USBcam import *
from face_recog_module import FaceRecog
from myparser import get_arguments
import cv2

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
    rec = FaceRecog()
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
    host, _= get_arguments()
    if not host:
        host = '192.168.0.6'
    app.run(host=host, port=7072, debug=True)


if __name__ == '__main__':
    stream_main()