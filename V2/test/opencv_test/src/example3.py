import time
import cv2

imagen = cv2.imread('logo.png')

time.sleep(0.1)

cv2.imshow("Image", imagen)
cv2.waitKey(0)
