import cv2
import numpy as np

position = []
color = ""

cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)

def on_mouse_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        global position
        position = [y, x]

cv2.setMouseCallback(
    window_name="Camera", 
    on_mouse=on_mouse_click
)

measures = []
bgr_color = []
hsv_colors = []
MEASURES_NUMBER = 10

while cam.isOpened():
    _, img = cam.read()
    img = cv2.flip(img, 1)
    # gray = cv2.GaussianBlur(gray, (21, 21), sigmaX=0)

    if position:
        pxl = img[position[0], position[1]]
        measures.append(pxl)
        if len(measures) >= MEASURES_NUMBER:
            bgr_color = np.uint8([[np.average(measures, 0)]])
            hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)

            bgr_color = bgr_color[0, 0]
            hsv_color = hsv_color[0, 0]

            hsv_colors.append(list(hsv_color))
            print(len(hsv_colors))

            measures.clear()

        cv2.circle(img, (position[1], position[0]), 10, (0, 0, 255), 2)
    
    if len(hsv_colors) > 20:
        hsv_colors = np.array(hsv_colors)
        print(hsv_colors.mean(axis=0))
        hsv_colors = []

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    
    # cv2.putText(img, f"Color BGR: {bgr_color}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (25, 50, 200))
    # cv2.putText(img, f"Color HSV: {hsv_color}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (25, 50, 200))

    cv2.imshow("Camera", img)
    
cam.release()
cv2.destroyAllWindows()
