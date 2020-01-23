from scipy import fftpack
import cv2
from PIL import Image
import os
import glob





################################################
# Transform image to grayscale
################################################
def grayscale(img): # Use in ROS
    #Load the image as colour image and convert it to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #print("Check gray")
    #print(gray)
    #print("Mean of grayscale value")
    #print(gray.mean())
    return gray

################################################
# Image Analysis to get brightness and contrast
# ToDo: Priyanka
################################################
def analysis(img): # use in ROS
    #cv2.meanStdDev function computes both mean and standard deviation simultaneously and it is used for image normalisation
    #meanstddev_img = cv2.meanStdDev(img)
    (means, stds) = cv2.meanStdDev(img)
    brightness = "Dark"
    if means >75:
        brightness = "Bright"
    print("Printing mean and std")
    print(means)
    print(stds)
    #print(meanstddev_img)
    # return meanstddev_img
    # ToDo: Decision Rule for Light or Dark Images
    cv2.putText(img, brightness, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), lineType=cv2.LINE_AA)
    cv2.imshow('Normalise Image', img)
    cv2.waitKey(0)

    return means, stds, brightness


################################################
# Find the brightness of the Image using HSV Model
# Colour Model: HSV
# HSV Colour Model: Hue, Saturation, Value
# Hue: the dominant color as perceived by the observer
# Saturation: the amount of white light mixed with a hue
# Value: the chromatic notion of intensity
# ToDo: Priyanka
################################################
def hsvModel_brightness(img, num):
    hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #
    #cv2.imshow("HSV Image", hsvImg)
    hue, sat, val = hsvImg[:, :, 0], hsvImg[:, :, 1], hsvImg[:, :, 2] #

    # calculate histogram of third channel V i.e val.
    #hist= cv2.calcHist([hsvImg], [2], None, [256], [0, 256])
    #plt.subplot(311)  # plot in the first cell
    #plt.title("Luminosity Value of Test" + str(num))
    #plt.hist(np.ndarray.flatten(val), bins=128)
    #plt.show()
    #Calculate mean of Val to get the average brightness of all the values of the pixels in Value as value determines the brightness in the image
    valMean = val.mean() #
    #print("Mean of value :" + str(valMean))
    brightness= "Dark"
    if valMean >100: #
        brightness = "Bright" #
    cv2.putText(img, brightness, (40, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), lineType=cv2.LINE_AA)
    #cv2.imshow('Image', img)
    return brightness, valMean



img_dir = 'C:/Users/Michael/PycharmProjects/Camera_Aggregator/testbilder/'
datapath = os.path.join(img_dir, '*png')
files = glob.glob(datapath)
print("Files: "+ str(files))





for imnum in files:
    #img = cv2.imread('testbilder/Test{}.png'.format(imnum))
    img = cv2.imread(imnum)
    #img = Image.open(imnum).convert('L')
    #print(img.shape)

    # Reduce the size of the image
    reducedImage = cv2.pyrDown(img)

    #hsvModel_brightness(img, imnum)
    #gray = grayscale(img) # use in ROS

    gray = grayscale(reducedImage)  # use in ROS
    contrast = analysis(gray)
    print(contrast)





