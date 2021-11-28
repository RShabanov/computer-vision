import cv2

BASE_PATH = "practice/find-difference/"

cat = cv2.imread(BASE_PATH + "cat.png")

cat1 = cv2.cvtColor(cat, cv2.COLOR_BGR2GRAY)
cat2 = cv2.imread(BASE_PATH + "cat2.png", 0)

diff = cv2.absdiff(cat1, cat2)

thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.dilate(thresh, None, iterations=2)
contours, hierarchy = cv2.findContours(thresh, 
                                          cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    (x, y, w, h) = cv2.boundingRect(cnt)
    cv2.rectangle(cat, (x, y), (x + w, y + h), (20, 255, 55), 2)
    
cv2.putText(cat, 
            f"Differences number: {len(contours)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0))

cv2.namedWindow("Original", cv2.WINDOW_KEEPRATIO)
cv2.namedWindow("Difference", cv2.WINDOW_KEEPRATIO)

cv2.imshow("Original", cat)
cv2.imshow("Difference", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()