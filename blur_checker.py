from scipy import fftpack
import cv2
import os
import glob
import numpy as np


################################################
# Transform image to grayscale
################################################
def grayscale(img): # Use in ROS
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

################################################
# Image Analysis to get brightness and contrast
# ToDo: Priyanka
################################################
def analysis(img): # use in ROS
    meanstddev_img = cv2.meanStdDev(img)
    # ToDo: Decision Rule for Light or Dark Images
    return meanstddev_img

################################################
# Run Laplacian Variation for blurry detection
################################################
def variance_of_laplacian(image): # Use in ROS, Return Sharpness Level
    fm = cv2.Laplacian(image, cv2.CV_64F).var()
    print("Laplacian")
    blurry = "CLEAR" # Not blurry
    if fm < 320: # Defined Threshold based on domain expert and application scenario
        blurry = "BLURRY" #blurry
    return blurry, fm

################################################
# Noise Detection in frequency domain(?)
# Noise Detection using Natural Scene Statistics
# ToDo:(Check and implement)
#Reduce noise by blurring with a Gaussian filter ( kernel size = 3 )
def reducenoise(image):
    noiseReducedimg = cv2.GaussianBlur(image, (3, 3), 0)
    return noiseReducedimg
################################################

################################################
# Noise Detection in frequency domain(?)
# Noise Detection using Natural Scene Statistics
# ToDo: Priyanka
################################################
def noise_detection():
    # ToDo: Search for detection method. Maybe use Low-Pass Filter (FFT) for this
    return 0

################################################
# Haze Analysis on Image
# ToDo: Priyanka
################################################
def haze_detection():
    # ToDo: Using Atmospheric Scattering Model, see Mao et al., 2014
    return 0

################################################
# Import Images from directory and run analysis
# Subscribe to ImageRaw_msg and run algorithm with 0.5Hz
# ToDo: Jacob
################################################

img_dir = 'C:/Users/Michael/PycharmProjects/Camera_Aggregator/testbilder/'
datapath = os.path.join(img_dir, '*png')
files = glob.glob(datapath)
print("Files: "+ str(files))


for imnum in files:
    #img = cv2.imread('testbilder/Test{}.png'.format(imnum))
    img = cv2.imread(imnum)
    gray = grayscale(img) # use in ROS
    contrast = analysis(gray)
    blurry, fm = variance_of_laplacian(gray)
    print(contrast)
    cv2.putText(img, '{}: {:.2f}'.format(blurry, fm), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255),3)
    cv2.imshow('Image', img)
    key = cv2.waitKey(0)


################################################
# Show Images and print results
# Write Data into InfluxDB given data scheme
# ToDO: Jacob
################################################



