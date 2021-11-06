import numpy as np
import matplotlib.pyplot as plt
from skimage import filters

lama = plt.imread("./practice/lama_on_moon.png")[21:-40, 45:-20]
lama = np.sum(lama, 2)

sobel = np.abs(filters.sobel(lama))
threshold = filters.threshold_otsu(sobel)
sobel[sobel < threshold] = 0
sobel[sobel > 0] = 1


plt.subplot(121)
plt.imshow(lama)
plt.subplot(122)
plt.imshow(sobel)
plt.show()