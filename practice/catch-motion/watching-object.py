import cv2
import numpy as np

cam = cv2.VideoCapture(0)

cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("ROI", cv2.WINDOW_KEEPRATIO)

roi = None

while cam.isOpened():
    _, img = cam.read()
    
    img = cv2.flip(img, 1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (21, 21), sigmaX=0)

    if roi is not None:
        res = cv2.matchTemplate(gray, roi, cv2.TM_CCORR_NORMED)
        # cv2.imshow("Match template", res)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        top_left = max_loc
        bottom_right = (top_left[0] + roi.shape[1],
                        top_left[1] + roi.shape[0])

        cv2.rectangle(img, top_left, bottom_right, (255, 0, 0), 2)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('r'):
        r = cv2.selectROI("ROI selection", gray)
        roi = gray[int(r[1]): int(r[1] + r[3]),
                    int(r[0]): int(r[0] + r[2])]

        cv2.imshow("ROI", roi)
        cv2.destroyWindow("ROI selection")
    cv2.imshow("Camera", img)
    
cam.release()
cv2.destroyAllWindows()
