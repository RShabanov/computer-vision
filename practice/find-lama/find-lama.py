import numpy as np
import matplotlib.pyplot as plt
from skimage import filters
from skimage.measure import regionprops, label

lama = plt.imread("./find-lama/lama_on_moon.png")[21:-40, 45:-20]
lama = np.sum(lama, 2)

sobel = np.abs(filters.sobel(lama))
threshold = filters.threshold_otsu(sobel)
sobel[sobel < threshold] = 0
sobel[sobel > 0] = 1

labeled = label(sobel)
region_max = None
for region in regionprops(labeled):
    if region_max is None or region_max.perimeter < region.perimeter:
        region_max = region

labeled[labeled != region_max.label] = 0

filled_image_full = np.zeros_like(sobel)
y, x, _, _ = region_max.bbox
filled_image_full[y:y+region_max.filled_image.shape[0], x:x+region_max.filled_image.shape[1]] = region_max.filled_image

result = np.logical_and(sobel, filled_image_full)

plt.subplot(121)
plt.imshow(lama)
plt.subplot(122)
plt.imshow(result)
plt.show()