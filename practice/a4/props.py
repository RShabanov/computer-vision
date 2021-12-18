import cv2
import numpy as np

image = cv2.imread("./practice/a4/imgs/arrow.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 10, 255, 0)

cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]

arrow = cnts[0]
# cv2.drawContours(image, cnts, -1, (255, 0, 0))

print(f"Area: {cv2.contourArea(arrow)}")
print(f"Perimeter: {cv2.arcLength(arrow, True)}")

moments = cv2.moments(arrow)
# print(f"Moments: {moments}") 

centroid = (int(moments["m10"] / moments["m00"]),
            int(moments["m01"] / moments["m00"]))

print(f"Centroid: {centroid}")
cv2.circle(image, centroid, 4, (255, 0, 0), 2)

eps = 0.002 * cv2.arcLength(arrow, True)
approx = cv2.approxPolyDP(arrow, eps, True)
for p in approx:
    cv2.circle(image, tuple(*p), 6, (0, 255, 0), 2)

hull = cv2.convexHull(arrow)
for i in range(1, len(hull)):
    cv2.line(image, tuple(*hull[i-1]), tuple(*hull[i]), (0, 255, 0), 2)
cv2.line(image, tuple(*hull[-1]), tuple(*hull[0]), (0, 255, 0), 2)


x, y, w, h = cv2.boundingRect(arrow)
cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 2)


rect = cv2.minAreaRect(arrow)
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(image, [box], 0, (125, 125, 75), 2)


(x, y), rad = cv2.minEnclosingCircle(arrow)
x = int(x)
y = int(y)
rad = int(rad)
cv2.circle(image, (x, y), rad, (255, 255, 0), 2)


ellipse = cv2.fitEllipse(arrow)
cv2.ellipse(image, ellipse, (255, 255, 255), 2)


vx, vy, x, y = cv2.fitLine(arrow, cv2.DIST_L2, 0, 0.01, 0.01)
lefty = int((-x*vy/vx) + y)
righty = int(((image.shape[0] - x) * vy / vx) + y)
cv2.line(image, (image.shape[0] - 1, righty), (0 , lefty), (0, 255, 0), 2)
print(lefty, righty)

cv2.namedWindow("img", cv2.WINDOW_KEEPRATIO)
cv2.imshow("img", image)

key = cv2.waitKey(0)
if key == ord('q'):
    cv2.destroyAllWindows()
