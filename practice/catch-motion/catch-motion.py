import cv2
import numpy as np

cam = cv2.VideoCapture(0)

cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Background", cv2.WINDOW_KEEPRATIO)

background = None
prev_gray = None
buffer = []
BUFFER_SIZE = 10

frames = 0

while cam.isOpened():
    _, img = cam.read()
    
    img = cv2.flip(img, 1)

    frames += 1
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), sigmaX=0)

    if frames % 10 == 0 and prev_gray is not None:
        diff = prev_gray - gray # try with image area
        buffer.append(diff.mean())
        frames = 0

    if len(buffer) > BUFFER_SIZE:
        buffer.pop(0)
        std = np.std(buffer)
        print(std)
        if std < 35:
            print("Updating background...")
            background = gray.copy()
            buffer.clear()
        
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
            if area > 600:
                (x, y, w, h) = cv2.boundingRect(cnt)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Background", thresh)
    cv2.imshow("Camera", img)
    prev_gray = gray
    
    
cam.release()
cv2.destroyAllWindows()
