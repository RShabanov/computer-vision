import cv2
import numpy as np
import time

cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)

lower_green = (50, 100, 150)
upper_green = (90, 255, 255)

prev_time = time.time()
curr_time = time.time()
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0
d = 5.6e-2 # m
radius = 1

while cam.isOpened():
    curr_time = time.time()

    _, img = cam.read()
    img = cv2.flip(img, 1)
    # blurred = cv2.GaussianBlur(img, (11, 11), sigmaX=0)

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv_img, lowerb=lower_green, upperb=upper_green)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (curr_x, curr_y), radius = cv2.minEnclosingCircle(c)

        if radius > 10:
            cv2.circle(img, (int(curr_x), int(curr_y)), int(radius), (0, 0, 255), 2)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

    time_diff = curr_time - prev_time
    pxl_per_m = d / radius

    dist = np.math.sqrt((prev_x - curr_x)**2 + (prev_y - curr_y)**2)
    speed = dist / time_diff * pxl_per_m
    
    cv2.putText(img, 
                f"Ball speed: {round(speed, 5)} m/s", 
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.7,
                (0, 0, 255),
                2)
    cv2.imshow("Camera", img)
    cv2.imshow("Mask", mask)

    prev_time = curr_time
    prev_x, prev_y = curr_x, curr_y
    
cam.release()
cv2.destroyAllWindows()
