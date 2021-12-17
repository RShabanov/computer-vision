import platform
import mss.tools as tools
from numpy.core.fromnumeric import mean
import pyautogui as pag
import webbrowser
import time
import cv2
import numpy as np
import os.path as path
from .rect import Rect

DINO_URL = "https://chromedino.com/"

SYSTEM = platform.system().lower()

# import mss for specific OS
if SYSTEM == "linux":
    from mss.linux import MSS as mss
elif SYSTEM == "windows":
    from mss.windows import MSS as mss
else:
    from mss.darwin import MSS as mss


def find_obstacles(cnts):
    def intersect(lhs, rhs):
        return rhs[0] <= lhs[0] <= rhs[0] + rhs[2] \
            or lhs[0] <= rhs[0] <= lhs[0] + lhs[2]

    # get all bboxes sorted by left X
    x_ranges = []
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        x_ranges.append((x, y, w, h))

    x_ranges.sort(key=lambda bound: bound[0])

    obstacles = []
    for curr in x_ranges:
        if len(obstacles) > 0:
            if intersect(obstacles[-1], curr):
                x = min(obstacles[-1][0], curr[0])
                y = min(obstacles[-1][1], curr[1])
                w = max(obstacles[-1][2], curr[2])
                h = max(obstacles[-1][-1], curr[-1])

                obstacles[-1] = (x, y, w, h)
                continue
        obstacles.append(curr)

    return obstacles


class Dino:
    def __init__(self) -> None:
        pass

    def run(self):
        # open the game
        webbrowser.open(DINO_URL)

        # delay for url loading
        time.sleep(5)

        with mss() as sct:
            field = self._find_field(sct)

            monitor = {
                "top": field.top_left.y, 
                "left": field.top_left.x, 
                "width": field.width, 
                "height": field.height
            }

            field = Rect(0, 0, field.width, field.height)

            prev_time = time.time()
            start_time = time.time()

            distance_threshold = 95

            # values from the game
            acceleration = 0.001
            acceleration_coeff = 2.4
            max_speed = 13
            speed = 6

            time_history = [0.00523 for _ in range(100)]

            pag.press("space")

            while "Screen capturing":
                curr_time = time.time()
                d_time = curr_time - prev_time
                time_history = time_history[1:] + [d_time]
                prev_time = curr_time

                # approximately
                # every 100 px or whatever it is
                if int(curr_time - start_time) % 11 == 10:
                    start_time = curr_time
                    acceleration += acceleration_coeff
                        
                # Get raw pixels from the screen, save it to a Numpy array
                img = np.array(sct.grab(monitor))

                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # simplify obstacles so that there are not many pieces
                img = cv2.dilate(img, (5, 5), iterations=2)
                img = cv2.erode(img, None, iterations=2)
                
                # edge algo - after this it doesn't matter whether it is a black or white mode
                img = cv2.Canny(img, threshold1=0, threshold2=255, apertureSize=3)

                cnts = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                obstacles = find_obstacles(cnts)
    
                if len(obstacles) > 1:
                    dino = Rect(*obstacles[0])
                    obstacle = Rect(*obstacles[1])

                    time_median = np.median(time_history)

                    if speed < max_speed:
                        speed += acceleration * time_median
                    else: speed = max_speed

                    threshold = distance_threshold + time_median * speed

                    # if there are more than 2 obstacles
                    if len(obstacles) > 2:
                        x, _, _, _ = obstacles[2]
                        x_mean = (obstacle.top_left.x + x) / 2

                        # and their pair distance is less than a half of `threshold`
                        # we have to shift obstacle left x so the dino jumps earlier
                        if x_mean < threshold / 2:
                            obstacle.top_left.x = x_mean / 4

                    dist = obstacle.top_left.x - dino.bottom_right.x

                    if dist < threshold:
                        if abs(monitor["height"] / 2 - obstacle.bottom_right.y) < 5:
                            pag.keyDown("down")
                            time.sleep(0.0035)
                            pag.keyUp("down")
                        else:
                            pag.press("space")
                            time.sleep(0.00523)

                self._debug(img, obstacles)

                key = cv2.waitKey(1)
                if key == ord('q'):
                    break

            cv2.destroyAllWindows()

    def _find_field(self, sct):
        width, height = pag.size()
        monitor = {"top": 0, "left": 0, "width": width, "height": height}

        img = np.array(sct.grab(monitor))

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_edge = cv2.Canny(img_gray, threshold1=0, threshold2=255)

        template_path = path.join("autotrex", "templates", "edge_dino_template.png")
        edge_dino_template = cv2.imread(template_path, 0) 


        matches = cv2.matchTemplate(img_edge, edge_dino_template, cv2.TM_CCOEFF_NORMED)
        _, maxVal, _, max_loc = cv2.minMaxLoc(matches)

        if maxVal < 0.6:
            raise Exception("T-Rex was not found")

        h, w = edge_dino_template.shape
        field_pos = Rect(max_loc[0], max_loc[1] + 1, 500 + w, h)

        return field_pos

    def _debug(self, img, obstacles):
        for cnt in obstacles:
            x, y, w, h = cnt
            cv2.rectangle(
                img,
                (x, y),
                (x + w, y + h),
                255,
                2
            )

        cv2.imshow("dino", img)