import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import dilation, erosion, square


def neighbours4(y, x):
    return (y, x+1), (y+1, x), (y, x-1), (y-1, x)

def neighbours8(y, x):
    return (y,x+1),(y+1,x+1),(y+1,x),(y+1,x-1),(y,x-1),(y-1, x-1),(y-1, x),(y-1,x+1)

def get_boundaries(LB, label=1):
    pxs = np.where(LB == label)
    boundaries = []
    
    for y, x in zip(*pxs):
        for yn, xn in neighbours4(y, x):
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

def sort_boundaries(boundaries):
    """
        since we need sorted boundaries for chain algorithm
        we have to sort result of function get_boundaries
    """
    nb = [boundaries[0]]
    dist = lambda p1, p2: (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

    while len(boundaries) != len(nb):
        min_d = float('inf')
        nearest_point = None

        for y, x in neighbours8(*nb[-1]):
            if (y, x) in boundaries and (y, x) not in nb:
                d = dist((y, x), nb[-1])
                if min_d >= d:
                    nearest_point = (y, x)
                    min_d = d
        nb.append(nearest_point)
    return nb

def chain_code(img, label: int=1) -> list:
    """
        we have 8 directions: N, E, W, S, NE, SE, SW, NW
    """
    chain = []
    boundaries = sort_boundaries(get_boundaries(img, label))
    
    for i in range(len(boundaries)):
        y, x = boundaries[i]
        neighbour_idx = i + 1 if i + 1 < len(boundaries) else 0
        y1, x1 = boundaries[neighbour_idx]

        """
            for moore neighborhood:
                3 2 1
                4 . 0
                5 6 7
        """
        code = None
        if y < y1:
            code = 5 if x > x1 else 7 if x < x1 else 6
        elif y > y1:
            code = 3 if x > x1 else 1 if x < x1 else 2
        else:
            code = 4 if x1 < x else 0
        chain.append(code)

    return chain

def difference_chain(chain_code: list) -> list:
    """
        we have 8 directions: N, E, W, S, NE, SE, SW, NW
    """
    MAX_VALUE = 8
    diff_chain = []
    for i in range(len(chain_code)):
        diff = chain_code[i-1] - chain_code[i]
        code = (MAX_VALUE - abs(diff)) if diff > 0 else abs(diff)
        diff_chain.append(code)
    return diff_chain

def normalize_chain(chain: list) -> list:
    chain = np.array(chain)
    idx_min = chain.argmin()
    return np.concatenate((chain[idx_min:], chain[:idx_min]), axis=0)

def show_figures(img, figures: list, mask):
    from math import ceil
    subplot_number = ceil(len(figures) / 2)
    
    fig, axs = plt.subplots(subplot_number, 2, figsize=(12, 8))
    fig.tight_layout(pad=3.0)

    total = 0

    for i, (number, label) in enumerate(figures):
        img_pxs = np.array(np.where(img == label))
        y_start, x_start = img_pxs.min(axis=1)
        y_end, x_end = img_pxs.max(axis=1)

        title = f"Quantity of figure: {number}"
        if subplot_number == 1:
            axs[i % 2].title.set_text(title)
            axs[i % 2].imshow(erosion(img[y_start-1:y_end+2, x_start-1:x_end+2], mask))
        else:
            axs[i >> 1, i % 2].title.set_text(title)
            axs[i >> 1, i % 2].imshow(erosion(img[y_start-1:y_end+2, x_start-1:x_end+2], mask))

        total += number
        
    if len(figures) % 2 != 0:
        plt.delaxes(axs[-1, -1])

    fig.suptitle(f"Total figure quantity: {total}")
    plt.show()


stars = np.load('./object-counting/ps.npy')
MASK = square(2)

labeled = label(dilation(stars, MASK))
print(f"Total number of figures: {labeled.max()}")

figures = dict()
for i in range(1, labeled.max()+1):
    boundaries = sort_boundaries(get_boundaries(labeled, label=i))
    cc = tuple(normalize_chain(difference_chain(chain_code(labeled, label=i))))

    if cc in figures:
        figures[cc][0] += 1
    else:
        figures[cc] = [1, i] # i - to show what kind of figure it is

show_figures(img=labeled, figures=figures.values(), mask=MASK)
