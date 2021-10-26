import numpy as np

img1 = np.loadtxt("img1.txt", skiprows=2, dtype=np.ubyte)
img2 = np.loadtxt("img2.txt", skiprows=2, dtype=np.ubyte)

def image_shift(img1: np.ndarray, img2: np.ndarray) -> tuple:
    nonzero_indices1 = img1.nonzero()
    nonzero_indices2 = img2.nonzero()

    y_shift = np.abs(nonzero_indices1[0].min() - nonzero_indices2[0].min())
    x_shift = np.abs(nonzero_indices1[1].min() - nonzero_indices2[1].min())

    return (y_shift, x_shift)

y_shift, x_shift = image_shift(img1, img2)
print("Image shift:")
print(f"y: {y_shift}")
print(f"x: {x_shift}")
