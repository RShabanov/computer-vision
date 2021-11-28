import cv2

cam = cv2.VideoCapture(0)

cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Background", cv2.WINDOW_KEEPRATIO)

background = None
while cam.isOpened():
    _, img = cam.read()
    
    img = cv2.flip(img, 1)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), sigmaX=0)
    
    cv2.imshow("Camera", gray)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('b'):
        background = gray.copy()
        
    if background is not None:
        delta = cv2.absdiff(background, gray)
        cv2.imshow("Background", delta)
    
    
cam.release()
cv2.destroyAllWindows()