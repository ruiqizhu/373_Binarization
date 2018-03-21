import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
if __name__ == '__main__':
    threshold = float(sys.argv[1])
    img = mpimg.imread('oocyte1.png')
    # print(img)
    gray = rgb2gray(img)
    print(len(gray))
    print(len(gray[0]))
    for row in range(0, len(gray)):
        for col in range(0, len(gray[row])):
            if gray[row][col] > threshold:
                gray[row][col] = 1
            else:
                gray[row][col] = 0
    # print(gray)
    plt.imshow(gray, cmap = plt.get_cmap('gray'))
    plt.show()