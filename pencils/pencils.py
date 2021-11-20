import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.filters.thresholding import threshold_isodata
from skimage.measure import regionprops, label
from pathlib import Path

total_pencil_number = 0

for image_path in sorted(Path.cwd().glob("./pencils/images/*.jpg")):
    image = plt.imread(image_path)
    
    # since sometimes there is a high consrast on the edges of the image
    # the easiest way to remove it is just to crop it
    image = image[40:-40, 40:-40]
    
    gray_img = rgb2gray(image)

    thresh = threshold_isodata(gray_img)
    binary = gray_img.copy() <= thresh
    
    labeled = label(binary)
    regions = regionprops(labeled)
    
    pencil_cnt = 0
    
    # just the magic numbers which make this thing work
    for i in range(len(regions)):
        if regions[i].eccentricity < 0.98 or \
        regions[i].equivalent_diameter <= 55.0:
            labeled[labeled == regions[i].label] = 0
        else:
            pencil_cnt += 1
        
    total_pencil_number += pencil_cnt
    
    # to see number of pencils for the current image
    # print(f"Number of pencils for {image_path.relative_to(Path.cwd())}: {pencil_cnt}")
    
print(f"Total number of pencils: {total_pencil_number}")