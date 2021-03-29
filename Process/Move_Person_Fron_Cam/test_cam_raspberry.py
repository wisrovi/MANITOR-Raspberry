
import time
import cv2

USE_RPI = False
#USE_RPI = True

if not USE_RPI:
    cap = cv2.VideoCapture(0)
else:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    # allow the camera to warmup
    time.sleep(0.1)
    # capture frames from the camera

    class Cam(object):
        def read(self):
            try:
                camara = camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)
                camara = camara.array
                rawCapture.truncate(0)
                return True, camara
            except:
                return False, None

    cap = Cam()

while True:
    ret, image = cap.read()

    # show the frame
    cv2.imshow("Frame", image)

    # if the `ESC` key was pressed, break from the loop
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
