import cv2
import numpy as np

# print(cv2.getBuildInformation())

news = cv2.imread("./practice/news/news.jpg")
chebu = cv2.imread("./practice/news/cheburashka.jpg")

rows, cols, _ = chebu.shape

pts1 = np.float32([
    [0, 0],
    [0, rows],
    [cols, 0],
    [cols, rows]
]) # chebu position to cut

pts2 = np.float32([
    [19, 25],
    [39, 294],
    [434, 51],
    [434, 266]
]) # TV position to cut

M = cv2.getPerspectiveTransform(pts1, pts2)

aff_img = cv2.warpPerspective(chebu, M, (cols, rows))[:300, :470]

for y in range(aff_img.shape[0]):
    for x in range(aff_img.shape[1]):
        if np.all(aff_img[y, x] == 0): continue
        news[y, x] = aff_img[y, x]

cv2.namedWindow("Image", cv2.WINDOW_KEEPRATIO)
cv2.imshow("Image", news)

cv2.waitKey(0)
cv2.destroyAllWindows()