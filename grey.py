import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys

dirs = [(-1, -1), (-1, 0), (-1, +1),
        ( 0, -1), ( 0, +1),(+1, -1),
        (+1, 0), (+1, +1)]

def pixelSpread(gray, clickXY, pix_val):
    col, row = clickXY
    print("coordinate is ", (row, col))
    for dir in dirs:
        newRow, newCol = row, col
        drow, dcol = dir
        while posLegal(newRow, newCol):
            print(newRow, newCol)
            gray[newRow][newCol] = pix_val
            newRow += drow
            newCol += dcol
    gray[0][0] = 0.3
    print("pixel spread complete")


def posLegal(newRow, newCol):
    return (newRow >= 0 and newRow < height and newCol >= 0 and newCol < width)


# calculate the greyscale value of each pixel
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def onclick(event):
    global gray
    clickXY = (0, 0) # the xy coordinate of user's click
    if event.xdata != None and event.ydata != None:
        clickXY = (int(event.xdata), int(event.ydata))
        fig.canvas.mpl_disconnect(cid)
        plt.close()
        pixelSpread(gray, clickXY, 0.5)
        new_gray = plt.imshow(gray, cmap = plt.get_cmap('gray'))
        print(gray)
        plt.show()
        return "I am done"



if __name__ == '__main__':
    image = sys.argv[1] # image file name
    threshold = float(sys.argv[2]) # threshold for black & white
    img = mpimg.imread(image)
    gray = rgb2gray(img)
    # print(gray)
    # show_gray = plt.imshow(gray, cmap = plt.get_cmap('gray'))
    # plt.show()
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
    # print(gray)
    plt.show()
