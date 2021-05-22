import cv2


cv2.namedWindow("webcam")
vc = cv2.VideoCapture(0)


while True:
    next, frame = vc.read()
    cv2.imshow("webcam", frame)
    if cv2.waitKey(50) >= 0:
        break;