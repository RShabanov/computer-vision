import cv2
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread("./practice/a4/imgs/defects.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 10, 255, 0)

cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
# cv2.drawContours(image, cnts, -1, (255, 0, 0))

rect = cnts[0]
hull = cv2.convexHull(rect)
for i in range(1, len(hull)):
    cv2.line(image, tuple(*hull[i-1]), tuple(*hull[i]), (0, 255, 0), 2)
cv2.line(image, tuple(*hull[-1]), tuple(*hull[0]), (0, 255, 0), 2)


indices = cv2.convexHull(rect, returnPoints=False)
defects = cv2.convexityDefects(rect, indices)

for p in defects:
    s, e, f, d, = p[0]
    # cv2.circle(image, tuple(*rect[s]), 6, (255, 0, 255), 2)
    # cv2.circle(image, tuple(*rect[e]), 6, (255, 255, 0), 2)
    # cv2.circle(image, tuple(*rect[f]), 6, (0, 255, 255), 2)

    # dist = (rect[s][0] - rect[e][0])**2 + (rect[s][1] - rect[e][1])**2
    # if d != dist:
    #     dist = (rect[s][0] - rect[f][0])**2 + (rect[s][1] - rect[f][1])**2
    #     if d != dist:
    #         dist = (rect[e][0] - rect[f][0])**2 + (rect[e][1] - rect[f][1])**2

    


    # cv2.line(image, tuple(*rect[e]), (0 , lefty), (0, 255, 0), 2)



cv2.namedWindow("img", cv2.WINDOW_KEEPRATIO)
cv2.imshow("img", image)

key = cv2.waitKey(0)
if key == ord('q'):
    cv2.destroyAllWindows()