import cv2
import glob
import os
from PIL import Image


##############################################
# Transform image to grayscale
################################################

def grayscaleFD(originalImage):
    grayImageFD = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    return grayImageFD


def slow_horizontal_variance(grayImageFD):  # Return average variance of horizontal lines of a grayscale image

    # print(grayImageFD.shape)
    # rint(grayImageFD.size)
    width, height = grayImageFD.size
    # print("width: "+ str(width)+ "\n height: "+ str(height))
    vars = []
    pix = grayImageFD.load()
    # print("Printing pix: \n")
    # print(pix)

    for y in range(height):
        row = [pix[x, y] for x in range(width)]
        # print("PIX rows")
        # print(row)
        mean = sum(row) / width  # Mean intensity or colour value of each pixel in a single image
        # print("Mean Value of Image" + str(mean))
        variance = sum([(x - mean) ** 2 for x in row]) / width
        vars.append(variance)
        horizontalVariance = sum(vars) / height

    imgFogType = decideFogOrGoodImage(mean, horizontalVariance)
    return horizontalVariance, mean, imgFogType


def decideFogOrGoodImage(hMean, var):
    if hMean > 14 and var <= 1450:
        # print("FOGGY Image:  " + imgName + "\n")
        imageType = "FOGGY Image"
    else:
        # print("GOOD Image:  " + imgName + "\n")
        imageType = "GOOD Image"
    return imageType


img_dir = 'C:/Users/Michael/PycharmProjects/Camera_Aggregator/testbilder/'
datapath = os.path.join(img_dir, '*png')
files = glob.glob(datapath)
print("Files: " + str(files))
data = []


for fogImg in files:
        imgName = os.path.basename(fogImg)
        im = Image.open(fogImg).convert('L')
        #im = Image.open("C:/Users/Michael/PycharmProjects/Camera_Aggregator/testbilder/Test31.png").convert('L')
        img = cv2.imread(fogImg)
        #im.show()
        var, hMean,imgType= slow_horizontal_variance(im)
        #print("Horizontal Variance: "+ str(var))
        #print("Image_Type: " + imgType)
        #print("Variance Mean: " + str(hMean)) # Findings : When the mean value is less than 14 it belongs to a Foggy image as there is less intensity and less colour value. So adding the additional if condition with mean filter
        fog = var < 1000

        fogImageType = decideFogOrGoodImage(hMean,var)

        if hMean > 14 and var <= 1450:
            print("FOGGY Image:  " + imgName+ "\n")
            cv2.putText(img, fogImageType, (40, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), lineType=cv2.LINE_AA)
            cv2.imshow('Image', img)
            # key = cv2.waitKey(0)
        else:
            print("GOOD Image:  " + imgName + "\n")

        #print('%5.0f - %5s - %s' % (var, fog and 'FOGGY' or 'SHARP', imgName))


        #key = cv2.waitKey(0)

