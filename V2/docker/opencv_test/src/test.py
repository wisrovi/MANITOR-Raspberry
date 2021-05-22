import cv2
import numpy as np

black = np.zeros([600, 300, 3], dtype=np.uint8)

cv2.imshow("Frame", black)
cv2.waitKey(0)