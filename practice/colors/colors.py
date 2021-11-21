import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import mean
from numpy.lib.arraysetops import unique
from skimage import color

img = plt.imread('practice/colors/balls.png')

img = color.rgb2hsv(img)


def get_colors(hsv_img):
    unique_vals = np.unique(hsv_img[:,:,0])
    
    colors = []
    dist = 0
    start_idx = 0
    
    epsilon = np.diff(unique_vals).mean()
    
    for i in range(1, unique_vals.shape[0]):
        d = abs(unique_vals[i] - unique_vals[i - 1])
        if abs(dist - d) > epsilon:
            dist = 0
            colors.append(unique_vals[start_idx:i].mean())
            start_idx = i
            
    colors.append(unique_vals[start_idx:].mean())
    return colors
    
print(f"Colors: {get_colors(img)}")

plt.figure()
plt.subplot(121)
plt.imshow(img)
plt.subplot(122)
plt.plot(np.unique(img[:, :, 0]), 'o')
plt.show()