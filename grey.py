import numpy as np
import pylab
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
import os

dirs = [(-1, -1), (-1, 0), (-1, +1),
        ( 0, -1), ( 0, +1),(+1, -1),
        (+1, 0), (+1, +1)]

def pixelSpread(gray, clickPos, pix_val):
    row, col = clickPos
    # No effect when clicked in the white area
    if (gray[row][col] == 1): return
    gray[row][col] = pix_val
    #print("coordinate is ", (row, col))
    for dir in dirs:
        drow, dcol = dir
        newRow, newCol = row + drow, col + dcol
        if (posLegal(newRow, newCol) and gray[newRow][newCol] not in [pix_val, 1]):
            pixelSpread(gray, (newRow, newCol), pix_val)


def posLegal(newRow, newCol):
    return (newRow >= 0 and newRow < height and newCol >= 0 and newCol < width)


# calculate the greyscale value of each pixel
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def onclick(event):
    global gray
    clickPos = (0, 0) # the xy coordinate of user's click
    if event.xdata != None and event.ydata != None:
        clickPos = (int(event.ydata), int(event.xdata))
        fig.canvas.mpl_disconnect(cid)
        plt.close()
        pixelSpread(gray, clickPos, 0.5)
        new_gray = plt.imshow(gray, cmap = plt.get_cmap('gray'))
        print(gray)
        plt.show()
        return "I am done"



if __name__ == '__main__':
    image = sys.argv[1] # image file name
    threshold = float(sys.argv[2]) # threshold for black & white
    img = mpimg.imread(image)
    gray = rgb2gray(img)
    height = len(gray)
    width = len(gray[0])
    for row in range(0, height):
        for col in range(0, width):
            if gray[row][col] > threshold:
                gray[row][col] = 1 # turn the pixel white
            else:
                gray[row][col] = 0 # turn the pixel black
    # Connecting mouse click event to the position clicked
    ax = plt.gca()
    fig = plt.gcf()
    implot = ax.imshow(gray, cmap = plt.get_cmap('gray'))
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    
