import math
import cv2
import os, sys
from PIL import Image
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
import csv

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def click_oocyte(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pt = (x,y)
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
    img_name = sys.argv[1] # image file name
    threshold = .4

    #Resize the image
    size = 648 , 486
    im = Image.open(img_name)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(img_name[:-4] + "_resized.png")
    original = mpimg.imread(img_name[:-4] + "_resized.png")
    #print(original)
    #Binarize the image if not already greyscale
    if(isinstance(original[0][0], np.ndarray)):
        gray = rgb2gray(original)
    else:
        gray = original
    #print(gray)
    height = len(gray)
    width = len(gray[0])
    for row in range(0, height):
        for col in range(0, width):
            if gray[row][col] > threshold:
                gray[row][col] = 1 # turn the pixel white
            else:
                gray[row][col] = 0 # turn the pixel black


    

    #Create a structuring element and filter the image
    selem = disk(25)
    img = closing(img_as_ubyte(gray), selem)
    

    #Read in the filtered image and label it
    img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary
    img = cv2.bitwise_not(img)
    connectivity = 100
    output = cv2.connectedComponentsWithStats(img, connectivity, cv2.CV_32S)
    binary_map = (img > 0).astype(np.uint8)

    #The first cell is the number of identified components
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

    #save labeled image
    #cv2.imshow('labeled', labeled_img)
    cv2.imwrite(img_name[:-4] + "_labeled.png", labeled_img)
    # cv2.setMouseCallback("labeled", click_oocyte)
    # cv2.waitKey()
    with open(img_name[:-4] + '_area.csv', 'w', newline='') as csvfile:
        areawriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(1, len(stats)):
            areawriter.writerow([np.array2string(stats[i][4]) + "," + np.array2string(centroids[i][0]) + "," + np.array2string(centroids[i][1])] )