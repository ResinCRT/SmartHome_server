import cv2
import time


class USBCam:
    def __init__(self, show=False, framerate=25, width=640, height=480):
        self.size = (width, height)
        print(self.size)
        self.show = show
        self.framerate = framerate

        self.cap = cv2.VideoCapture(0) #0번카메라
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.size[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.size[1])
        # self.cap.set(cv2.CAP_PROP_FPS, self.framerate)


    def snapshot(self):#jpeg 이미지 1장 리턴
        retval, frame = self.cap.read() #프레임 캡쳐, frame:numpy 배열 - BGR
        if retval:
            _, jpg = cv2.imencode('.jpg', frame)
            return jpg.tobytes()
        return frame

    def get_raw_frame(self):
        retval, frame = self.cap.read()

        return retval, frame

    def run(self):
        while True:
            ret, img = self.cap.read()

            if ret:
                frame = cv2.imencode('.jpg', img)[1].tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                break


class MJpegStreamCam(USBCam):
    def __init__(self, show=True, framerate = 25, width = 640, height=480):
        super().__init__(show=show,framerate=framerate,width=width,height=height)

    
    def __iter__(self): #열거가능 객체이기 위한 조건 for x in MJpegStreamCam():
        self.run()

    def run(self):
        if self.show:
            while True:
                retval, frame = self.cap.read()
                if retval:
                    _, jpg = cv2.imencode('.JPG', frame)
                    yield (
                        (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpg + b'\r\n')
                    )
                else:
                    break

            
if __name__ == '__main__':
    # cam = USBCam(width=480, height=360)
    cam = USBCam()
    print(cam)

    while True:
        ret, fr = cam.cap.read()

        # show the frame
        cv2.imshow("Frame", fr)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    print('finish')