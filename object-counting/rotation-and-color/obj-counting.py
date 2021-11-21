import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops, label
from skimage import color
from enum import Enum, auto

class Color(Enum):
    RED = auto()
    ORANGE = auto()
    YELLOW = auto()
    GREEN = auto()
    TURQUOISE = auto()
    BLUE = auto()
    PURPLE = auto()    

    def detect_color(hue):
        if 0 <= hue <= 1:
            if hue < 0.0555:
                return Color.RED
            elif hue < 0.1111:
                return Color.ORANGE
            elif hue < 0.2083:
                return Color.YELLOW
            elif hue < 0.4583:
                return Color.GREEN
            elif hue < 0.5277:
                return Color.TURQUOISE
            elif hue < 0.7638:
                return Color.BLUE
            elif hue < 0.9166:
                return Color.PURPLE
            else:
                return Color.RED
        return None


def count_figures(regions, figures):
    for i in range(len(regions)):
        min_row, min_col, max_row, max_col = regions[i].bbox        
        figure_colors = np.unique(hsv_img[min_row:max_row, min_col:max_col, 0])
        
        if figure_colors.size > 0:
            area = (max_row - min_row) * (max_col - min_col)
            
            # if it is a circle
            if area != regions[i].area:
                key_color = Color.detect_color(figure_colors[-1])
                
                if key_color in figures["Circles"]:
                    figures["Circles"][key_color] += 1
                else:
                    figures["Circles"][key_color] = 1
                    
            # otherwise it is a rectangle
            else:
                key_color = Color.detect_color(figure_colors[-1])
                
                if key_color in figures["Rectangles"]:
                    figures["Rectangles"][key_color] += 1
                else:
                    figures["Rectangles"][key_color] = 1

def print_figures(figures):
    for key in figures:
        print(f"{key}: {'{'}")
        
        for color in figures[key]:
            color_name = ""
            if color == Color.RED: color_name = "red"
            elif color == Color.ORANGE: color_name = "orange"
            elif color == Color.YELLOW: color_name = "yellow"
            elif color == Color.GREEN: color_name = "green"
            elif color == Color.TURQUOISE: color_name = "turquoise"
            elif color == Color.BLUE: color_name = "blue"
            elif color == Color.PURPLE: color_name = "purple"
            
            print(f"\t{color_name}: {figures[key][color]}")
        print("}")


image = plt.imread("./object-counting/rotation-and-color/balls_and_rects.png")
hsv_img = color.rgb2hsv(image)

binary = np.sum(image, 2)
binary[binary > 0] = 1

labeled = label(binary)
regions = regionprops(labeled)

figures = {
    "Rectangles": dict(),
    "Circles": dict()
}

count_figures(regions, figures)                

print(f"Total number of figures: {labeled.max()}")
print_figures(figures)
