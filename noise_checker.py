import cv2
import glob
import os
from skimage.restoration import estimate_sigma
import math
import numpy as np
from scipy.signal import convolve2d


###############################################
# Transform image to grayscale
################################################

def grayscale(originalImage):
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    return grayImage

def estimate_noise(image):
    estimate = estimate_sigma(image, multichannel=True, average_sigmas=True)  #High value of "estimate" mean low noise.
    return estimate

def noise_detection(grayNoisyImg):
    Height, Width = grayNoisyImg.shape

    M = [[1, -2, 1],
         [-2, 4, -2],
         [1, -2, 1]]

    sigma = np.sum(np.sum(np.absolute(convolve2d(grayNoisyImg, M))))
    sigma = sigma * math.sqrt(0.5 * math.pi) / (6 * (Width - 2) * (Height - 2))
    return sigma


def noiseInImages(image, algo):
    if algo==1 :
        noiseLevel=estimate_noise(image)
    else:
        noiseLevel= noise_detection(image)

    return noiseLevel

def determineImageTypeBasedOnNoiseLevel(noise):
    if noise <= 3.4:
        #print("Low Noise In Image \n ")
        imageType = "LowNoise"
    else:
        if noise <=7:
            #print ("Medium Noise In Image \n")
            imageType = "MediumNoise"
        else:
            if noise >7:
                #print("High Noise In Image \n ")
                imageType = "HighNoise"
    return imageType

img_dir = 'C:/Users/Michael/PycharmProjects/Camera_Aggregator/testbilder/'
datapath = os.path.join(img_dir, '*png')
files = glob.glob(datapath)
data = []


for f1 in files:
        img=cv2.imread(f1)
        print(os.path.basename(f1))
        #print(os.path.split(f1)[-1])
        img = cv2.pyrDown(img)
        data.append(img)
        #cv2.imshow("Original_Image",img)

        grayImg = grayscale(img)
        cv2.imshow("Gray_Image",grayImg)

        algo=1
        noise= noiseInImages(grayImg,algo)
        #print("Noise: "+ str(noise))
        determineImageTypeBasedOnNoiseLevel(noise)

        key = cv2.waitKey(0)

