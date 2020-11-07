from USBcam import USBCam
import face_recog_module as frm
import cv2


class FaceCam(USBCam):
    def __init__(self):
        super().__init__(show=True)
        self.recog = frm.FaceRecog(self.cap)

    def run(self):
        while True:
            frame = self.recog.get_jpg_bytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == "__main__":
    cam = FaceCam()
    print(cam.recog.known_face_names)
    while True:
        frame = cam.recog.get_frame()

        # show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    print('finish')