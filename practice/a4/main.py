import cv2
import numpy as np

cam = cv2.VideoCapture(0)

# cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, -1)

cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Cnts", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Background", cv2.WINDOW_KEEPRATIO)

background = None

while cam.isOpened():
    _, image = cam.read()
    image = cv2.flip(image, 1)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)

    canny = cv2.Canny(blurred, 55, 105)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('b'):
        background = gray.copy()

    if background is not None:
        delta = cv2.absdiff(background, gray)
        thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1200:
                (x, y, w, h) = cv2.boundingRect(cnt)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Background", thresh)
        cv2.bitwise_not(canny, thresh)

    cv2.imshow("Camera", image)
    cv2.imshow("Cnts", canny)

cam.release()
cv2.destroyAllWindows()
