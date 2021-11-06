import numpy as np
import matplotlib.pyplot as plt
from skimage import draw
from skimage.filters import gaussian, threshold_otsu, threshold_local, threshold_yen, threshold_li

def hist(array):
  h = np.zeros(256)
  for i in range(array.shape[0]):
    for j in range(array.shape[1]):
      h[array[i, j]] += 1
  return h

def find_extrema(array):
  extrema = []
  for i in range(1, len(array) -1, 1):
    if array[i - 1] < array[i] > array[i + 1]:
      extrema.append(i)
  return extrema

# image = np.zeros((1000, 1000), dtype='uint8')
# image[:] = np.random.randint(20, 75, size=image.shape)

# rr, cc = draw.disk((500, 500), 90)
# image[rr, cc] = np.random.randint(100, 200, size=len(rr))

# rr, cc = draw.disk((100, 100), 90)
# image[rr, cc] = np.random.randint(220, 240, size=len(rr))

# image = (gaussian(image, sigma=1) * 255).astype('uint8')
# threshold = threshold_otsu(image)
# binary_image = image.copy()
# binary_image[binary_image < threshold] = 0
# binary_image[binary_image >= threshold] = 1

# h = hist(image)
# extrema = find_extrema(h)
# extrema_vals = h[extrema]
# std = np.std(extrema_vals)
# new_extrema = []
# for i in range(len(extrema_vals)):
# 	if extrema_vals[i] > 0.5 * std:
# 		new_extrema.append(i)
# print(new_extrema)

# plt.figsize=((10, 10))
# plt.subplot(131)
# plt.imshow(image)
# plt.subplot(132)
# # plt.plot(h)
# # plt.twinx()
# # plt.plot(np.diff(h), color='r')
# # plt.plot(new_extrema, 'o', color='g')
# # plt.subplot(133)
# plt.imshow(binary_image)
# plt.show()

image = plt.imread("./practice/coins.jpg")
gray = np.mean(image, axis=2).astype("uint8")

mean_row = np.mean(gray, axis=0)
mean_col = np.mean(gray, axis=1)
gray = np.divide(gray, mean_row)

th1 = gray.copy() > threshold_local(gray, 101)
th2 = gray.copy() > threshold_otsu(gray)
th3 = gray.copy() > threshold_li(gray)
th4 = gray.copy() > threshold_yen(gray)

plt.subplot(151)
plt.imshow(gray)

plt.subplot(152)
plt.imshow(th1)

plt.subplot(153)
plt.imshow(th2)

plt.subplot(154)
plt.imshow(th3)

plt.subplot(155)
plt.imshow(th4)
# # plt.plot(hist(gray))
plt.show()