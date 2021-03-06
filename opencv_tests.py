import math
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

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def click_oocyte(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:
		pt = (x,y)
		print(pt)
		min_dist = -1
		mindex = -1
		for i in range(0, int(centroids.size / 2) , 1):
			dist = distance(pt, centroids[i])
			if(dist < min_dist or min_dist == -1):
				min_dist = dist
				mindex = i
		print(mindex)
		return mindex

# calculate the greyscale value of each pixel
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

if __name__ == '__main__':
	#Read in the image
	orig_phantom = img_as_ubyte(io.imread( "binary.png", as_grey = True))
	#fig, ax = plt.subplots()

	#Perform the filtering
	selem = disk(14)
	img = dilation(orig_phantom, selem)
	selem2 = disk(8)
	img = erosion(img, selem2)
	#ax.imshow(closed, cmap=plt.cm.gray)

	#Read in the filtered image and label it
	#img = cv2.imread('filtered.png', 0)
	
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
	blank_ch = 255*np.ones_like(label_hue)
	labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

	# cvt to BGR for display
	labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

	# set bg label to black
	labeled_img[label_hue==0] = 255

	print("Num labels: " + str(num_labels))
	print("Stats: " + str(stats))
	print("Centroids: " + str(centroids))


	cv2.imshow('labeled', labeled_img)
	cv2.setMouseCallback("labeled", click_oocyte)
	cv2.waitKey()