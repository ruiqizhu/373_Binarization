
import cv2
import numpy as np
import pylab
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
import os
from skimage.data import data_dir
from skimage.util import img_as_ubyte
from skimage import io
from skimage.morphology import erosion, dilation, opening, closing, white_tophat
from skimage.morphology import black_tophat, skeletonize, convex_hull_image
from skimage.morphology import disk

# src = cv2.imread("test.png", 0)
# binary_map = (src > 0).astype(np.uint8)
# connectivity = 4 # or whatever you prefer

# output = cv2.connectedComponentsWithStats(binary_map, connectivity, cv2.CV_32S)
# num_labels = output[0]
# # The second cell is the label matrix
# labels = output[1]
# # The third cell is the stat matrix
# stats = output[2]
# # The fourth cell is the centroid matrix
# centroids = output[3]
# print("Num labels: " + str(num_labels))
# print("Labels: " + str(labels))
# print("Stats: " + str(stats))
# print("Centroids: " + str(centroids))
orig_phantom = img_as_ubyte(io.imread( "test.png", as_grey = True))
fig, ax = plt.subplots()

selem = disk(25)
closed = closing(orig_phantom, selem)
ax.imshow(closed, cmap=plt.cm.gray)



img = cv2.imread('filtered.png', 0)
img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary
img = cv2.bitwise_not(img)
connectivity = 4 # or whatever you prefer
output = cv2.connectedComponentsWithStats(img, connectivity, cv2.CV_32S)
binary_map = (img > 0).astype(np.uint8)

#ret, labels = cv2.connectedComponents(img)

num_labels = output[0]
# The second cell is the label matrix
labels = output[1]
# The third cell is the stat matrix
stats = output[2]
# The fourth cell is the centroid matrix
centroids = output[3]


# Map component labels to hue val
label_hue = np.uint8(179*labels/np.max(labels))
#label_hue = np.uint8(179*num_labels/np.max(num_labels))
blank_ch = 255*np.ones_like(label_hue)
labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

# cvt to BGR for display
labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

# set bg label to black
labeled_img[label_hue==0] = 0

print("Num labels: " + str(num_labels))
print("Labels: " + str(labels))
print("Stats: " + str(stats))
print("Centroids: " + str(centroids))
cv2.imshow('labeled.png', labeled_img)
cv2.waitKey()