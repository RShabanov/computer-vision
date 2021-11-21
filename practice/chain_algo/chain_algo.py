import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops, label

def neighbours4(y, x):
    return (y-1, x), (y, x+1), (y+1, x), (y, x-1)

def neighbors8(y, x):
    return (y-1, x), (y-1, x+1), (y, x+1), (y+1, x+1), (y+1, x), (y+1, x-1), (y, x-1), (y-1, x-1)

def get_boundaries(region):
    image = region.image * region.label
    label = region.label
    pos = np.where(image == label)
    boundaries = []
    
    for y, x in zip(*pos):
        for yn, xn in neighbours4(y, x):
            if yn < 0 or yn > image.shape[0]-1:
                boundaries.append((y, x))
                break
            elif xn < 0 or xn > image.shape[1]-1:
                boundaries.append((y, x))
                break
            elif image[yn, xn] != label:
                boundaries.append((y, x))
                break
    return boundaries

def chain_algo(region):
    bounds = get_boundaries(region)
    bounds.append(bounds[0])

    return _chain(bounds)

def _chain(bounds):
    dirs = []
    bounds_len = len(bounds)
    
    if bounds_len > 0:
        y, x = bounds[0]
        del bounds[0]
        
        while bounds_len != len(dirs):
            for n, (ny, nx) in enumerate(neighbors8(y, x)):
                if (ny, nx) in bounds:
                    dirs.append(n)
                    y, x = ny, nx
                    del bounds[bounds.index((ny, nx))]
                    break
            else: break
    return dirs

def curvature(chain):
    result = []

    for i in range(len(chain)):
        diff = chain[i-1] - chain[i]
        result.append(diff)

    for i in range(len(chain)):
        result[i] = result[i] % 8
    return result

def match(lhs, rhs):
    # use slices
    if len(lhs) == len(rhs):
        for i in range(0, len(lhs)):
            if np.all(lhs[i:] == rhs[:-i]) == np.all(lhs[:i] == rhs[-i:]):
                return True
    return False


image = np.load("./practice/chain_algo/similar.npy")

labeled = label(image)
regions = regionprops(labeled)

chains = []

plt.imshow(labeled)
plt.show()

for i in range(labeled.max()):
    is_match = False

    chain = curvature(chain_algo(regions[i]))
    for n in range(len(chains)):
        if match(chain, chains[n]):
            is_match = True
            break
    if not is_match:
        chains.append(chain)
        
    
print(f"Number of objects: {len(chains)}")
