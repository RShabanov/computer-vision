import cv2
from random import shuffle

cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)

hsv_colors = {
    "G": ((50, 100, 150), (90, 255, 255)),
    "Y": ((25, 50, 150), (33, 255, 255)),  
    "B": ((94, 252, 178), (98, 255, 255)),  
    "R": ((130, 120, 160), (180, 255, 255))
}

right_order = ['G', 'Y', 'B', 'R']
shuffle(right_order)

right_ordered_colors = []

print(f"Color order: {right_order}")

masks = [None for _ in range(len(hsv_colors))]

def draw_dots(img, colors, ratio=8):
    img_shape = img.shape[:-1]
    x, y = img_shape[1] // ratio, img_shape[0] // ratio
    width, height = img_shape[1] - 2 * img_shape[1] // ratio, img_shape[0] - 2 * img_shape[0] // ratio

    for i in range(2):
        for j in range(2):
            cv2.circle(img, (x + width * j, y + height * i), 15, colors[i * 2 + j], 2)


    # cv2.rectangle(img, lowerb_rect, upperb_rect, (0, 255, 0))

while cam.isOpened():
    _, img = cam.read()
    img = cv2.flip(img, 1)
    img = cv2.GaussianBlur(img, (11, 11), sigmaX=0)

    draw_dots(img, right_order)

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # balls = []
    
    for i, (lowerb, upperb, color) in enumerate(hsv_colors):
        masks[i] = cv2.inRange(hsv_img, lowerb, upperb)
        masks[i] = cv2.erode(masks[i], None, iterations=3)
        masks[i] = cv2.dilate(masks[i], None, iterations=3)

        cnts = cv2.findContours(masks[i], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            (curr_x, curr_y), radius = cv2.minEnclosingCircle(c)

            if radius > 12.5:
                cv2.circle(img, (int(curr_x), int(curr_y)), int(radius), (0, 0, 255), 2)
    #     else:
    #         masks[i] = None
        
    # if balls:
    #     ordered_seq = sorted(balls, key=lambda ball: ball[0][0])
    #     color_seq = [color for (_, color) in ordered_seq]

    #     if is_correct_seq(color_seq, right_order):
    #         cv2.putText(img, 
    #                     f"Correct", 
    #                     (10, 60),
    #                     cv2.FONT_HERSHEY_SIMPLEX, 
    #                     0.7,
    #                     (0, 0, 255),
    #                     2)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    # elif key == ord('o'):
    #     print(f"Current color seq: {color_seq}")

    cv2.imshow("Camera", img)

cam.release()
cv2.destroyAllWindows()
