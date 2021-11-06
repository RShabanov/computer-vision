import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label


def show_imgs(img, o_img):
    plt.subplot(121)
    plt.imshow(img)
    plt.subplot(122)
    plt.imshow(o_img)
    # plt.colorbar()
    plt.show()

def match(a, masks):
    for mask in masks:
        if np.all(a == mask):
            return True
    return False

def euler(img, label):
    corner_mask = np.array(
        [[0, 0],
         [0, label]], dtype='uint')
    invert_corner_mask = np.array(
        [[0, label],
         [label, label]], dtype='uint')

    X, Y = 0, 0

    label_idx = np.where(img == label)

    for y in range(label_idx[0].min() - 1, label_idx[0].max() + 1):
        for x in range(label_idx[1].min() - 1, label_idx[1].max() + 1):
            sub = img[y:y+2, x:x+2]

            if match(sub, [corner_mask]): X += 1
            elif match(sub, [invert_corner_mask]): Y += 1
    return X - Y

def neighbours(y, x):
    return (y, x+1), (y+1, x), (y, x-1), (y-1, x)

def get_boundaries(LB, label=1):
    pxs = np.where(LB == label)
    boundaries = []
    
    for y, x in zip(*pxs):
        for yn, xn in neighbours(y, x):
            if yn < 0 or yn > LB.shape[0]-1:
                boundaries.append((y, x))
                break
            elif xn < 0 or xn > LB.shape[1]-1:
                boundaries.append((y, x))
                break
            elif LB[yn, xn] != label:
                boundaries.append((y, x))
                break
    return boundaries

def get_chain(img, label):
    label_idx = np.where(img == label)
    chain = []

    boundaries = get_boundaries(img, label)

    for i in range(len(boundaries) - 1):
        y, x, ny, nx = boundaries[i], boundaries[i+1]

        # 7 0 1
        # 6 . 2
        # 5 4 3

        # TODO: finish
        chain.append()




    


def task_with_holes():
    holes_img = np.load('holes.npy').astype('uint')
    labeled = label(holes_img)
    for label in range(1, labeled.max() + 1):
        print(f"For label #{label} number of holes: {1 - euler(labeled, label)}")

    show_imgs(holes_img, labeled)

def task_with_similar():
    similar_img = np.load('similar.npy').astype('uint')
    labeled = label(similar_img)

    chains = []

    for label in range(1, labeled.max() + 1):
        chains.append(get_chain(labeled, label))

    plt.imshow(similar_img)
    plt.show()

task_with_similar()
