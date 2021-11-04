import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label

stars = np.load('ps.npy')

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

def draw_boundaries(LB, label=1):
    BB = np.zeros_like(LB)
    pos = np.where(LB == label)
    BB[pos] = LB[pos]
    
    for y, x in get_boundaries(BB, label):
        BB[y, x] = label + 1
    return BB

labeled = label(stars)
# plt.imshow(draw_boundaries(labeled, label=2))
# plt.show()
# print(get_boundaries(labeled))

cc1 = [0,0,0,0,0,6,6,6,4,2,3,4,5,6,4,2,2,2]
cc2 = [0,0,0,6,4,5,6,7,0,6,4,4,4,2,2,2,2,2]

def get_diff(lhs, rhs):
    diff = abs(lhs - rhs)
    # or 8
    return 4 - diff if lhs > rhs else diff

def get_fd(cc):
    fd = []
    for i in range(len(cc)):
        fd.append(get_diff(cc[i-1], cc[i]))
    return fd

def norm(cc):
    fd = np.array(get_fd(cc))
    idx_min = fd.argmin()
    norm_chain = np.concatenate((fd[idx_min:], fd[:idx_min]), axis=0)
    return norm_chain

def distance(p1, p2):
    return abs((p1[0] - p1[1]) + (p2[0] - p2[0]))

def get_chain_code(boundaries):
    chain_code = []
    for i in range(len(boundaries) - 1):
        y0, x0 = boundaries[i]
        y1, x1 = boundaries[i+1]

        code = None

        if y0 > y1:
            code = (distance((y0, x0), (y1, x1)) - 1) % 8
            # code = 1
        elif y0 < y1:
            code = 8 - (distance((y0, x0), (y1, x1)) + 1) % 8
            # code = 3
        else:
            code = 4 if x1 < x0 else 0

        chain_code.append(code)
    return chain_code


# boundaries = get_boundaries(labeled, label=2)
# chain_code = get_chain_code(boundaries)
# print(norm(chain_code))

print(norm(cc1))
print(norm(cc2))

