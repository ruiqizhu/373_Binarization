import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys

# the xy coordinate of user's click
clickXY = (0, 0)

# calculate the greyscale value of each pixel
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def onclick(event):
    global clickXY;
    if event.xdata != None and event.ydata != None:
        print(event.xdata, event.ydata)
        clickXY = (int(event.xdata), int(event.ydata))
        print(clickXY)
        fig.canvas.mpl_disconnect(cid)
        plt.close()
        return clickXY



if __name__ == '__main__':
    image = sys.argv[1] # image file name
    threshold = float(sys.argv[2]) # threshold for black & white
    img = mpimg.imread(image)
    gray = rgb2gray(img)
    show_grey = plt.imshow(gray, cmap = plt.get_cmap('gray'))
    plt.show()
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
    # plt.show()
