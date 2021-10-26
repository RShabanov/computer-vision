import numpy as np
import pathlib

figure_files = []
for file in pathlib.Path().glob("figure*.txt"):
    if file.is_file(): figure_files.append(file.name)

for figure_file in figure_files:
    mm = 0
    # read mm number
    with open(figure_file) as file:
        mm = np.float64(file.readline())

    img = np.loadtxt(figure_file, skiprows=2, dtype='uint8')

    nonzero_indices = img.nonzero()
    if nonzero_indices[1].size > 0:
        col_ap = nonzero_indices[1].min()
        col_disap = nonzero_indices[1].max()
        print(f"For image (path: {figure_file}) nominal resolution: {mm / (col_disap - col_ap)}")
    else:
        print(f"Image (path: {figure_file}) is empty")
