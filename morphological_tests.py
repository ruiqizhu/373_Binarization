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


def plot_comparison(original, filtered, filter_name):
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4), sharex=True,
                                   sharey=True)
    ax1.imshow(original, cmap=plt.cm.gray)
    ax1.set_title('original')
    ax1.axis('off')
    ax2.imshow(filtered, cmap=plt.cm.gray)
    ax2.set_title(filter_name)
    ax2.axis('off')
    plt.show()

if __name__ == '__main__':
	orig_phantom = img_as_ubyte(io.imread( "test.png", as_grey = True))
	fig, ax = plt.subplots()
	ax.imshow(orig_phantom, cmap=plt.cm.gray)
	selem = disk(25)
	#Dilation - separates well, doesn't preserve size well
	#dilated = dilation(orig_phantom, selem)
	
	#Closing - preserves size, separates oocytes ok
	closed = closing(orig_phantom, selem)
	
	#Opening - really bad, not useful at all
	#opened = opening(orig_phantom, selem)

	#Skeletonizing - just looks cool
	#sk = skeletonize(orig_phantom == 0)

	plot_comparison(orig_phantom, closed, 'closing')

