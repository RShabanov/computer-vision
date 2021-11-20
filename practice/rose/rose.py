import cv2
import numpy as np


# cam = cv2.VideoCapture(0)
# if cam.isOpened():
#     ret, frame = cam.read()
#     print(frame.shape)
# cam.release()

# mushroom = cv2.imread("./practice/mushroom.jpg")
# logo = cv2.imread("./practice/cvlogo.png")

# logo = cv2.resize(logo, (logo.shape[0] // 2, logo.shape[1] // 2))

# gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
# ret, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

# roi = mushroom[:logo.shape[0], :logo.shape[1]]
# mask_inv = cv2.bitwise_not(mask)

# bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
# fg = cv2.bitwise_and(logo, logo, mask=mask)

# combined = cv2.add(fg, bg)
# mushroom[:combined.shape[0], :combined.shape[1]] = combined


### ROSE
rose = cv2.imread("./practice/rose.jpg")

lower = np.array([0, 100, 100])
upper = np.array([0, 255, 255])

hsv = cv2.cvtColor(rose, cv2.COLOR_BGR2HSV)

mask = cv2.inRange(hsv, lower, upper)
res = cv2.bitwise_and(rose, rose, mask=mask)


cv2.namedWindow("Image", cv2.WINDOW_KEEPRATIO)
cv2.imshow("Image", res)

cv2.waitKey(0)
cv2.destroyAllWindows()

