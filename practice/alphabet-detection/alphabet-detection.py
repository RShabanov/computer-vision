import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

def lakes_and_bays(image):
    b = ~image
    lb = label(b)
    regs = regionprops(lb)

    count_lakes = 0
    count_bays = 0

    for reg in regs:
        on_bound = False
        for y, x in reg.coords:
            if y == 0 or x == 0 or \
                y == image.shape[0]-1 or \
                x == image.shape[1]-1:
                on_bound = True
                break
        if not on_bound:
            count_lakes += 1
        else:
            count_bays += 1
    return count_lakes, count_bays

def has_vline(image):
    lines = np.sum(image, axis=0) // image.shape[0]
    return 1 in lines

def filling_factor(image):
    return np.sum(image) / image.size

def recognize(region):
    if np.all(region.image):
        return '-'
    lakes, bays = lakes_and_bays(region.image)
    if lakes == 2:
        if has_vline(region.image):
            return "B"
        else:
            return "8"
    elif lakes == 1:
        if bays == 3:
            return "A"
        else:
            return "0"
    elif lakes == 0:
        if bays == 2:
            return "/"
        elif bays == 3 and has_vline(region.image):
            return "1"

        cut_lakes, cut_bays = lakes_and_bays(region.image[2:-2, 2:-2])
        if cut_bays == 4:
            return "X"
        elif cut_bays == 5:
            cy = region.image.shape[0] // 2
            cx = region.image.shape[1] // 2
            if region.image[cy, cx] > 0:
                return "*"
            return "W`"
    return None

image = plt.imread("./practice/alphabet.png")
binary = np.sum(image, 2)
binary[binary > 0] = 1

labeled = label(binary)
print(f"Object number: {labeled.max()}")

regions = regionprops(labeled)

d = {None: 0}
for region in regions:
    symbol = recognize(region)
    if symbol is not None:
        labeled[np.where(labeled == region.label)] = 0
    # else:
        # print(f"Filling factor: {filling_factor(region.image)}")
    if symbol not in d:
        d[symbol] = 0
    d[symbol] += 1
    
print(d)
print(f"Accuracy: {round((1. - d[None] / sum(d.values())) * 100, 2)}")
# print(lakes_and_bays(regions[72]))


plt.imshow(labeled)
# plt.imshow(regions[73].image, cmap='gray')
plt.show()