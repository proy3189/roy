import PIL.Image as imgpil
from pandas import DataFrame
from noise_checker import grayscale, noiseInImages, determineImageTypeBasedOnNoiseLevel
from fog_checker import slow_horizontal_variance
from brightness_checker import hsvModel_brightness
from blur_checker import variance_of_laplacian



class image_processing:

    def writeImageDetails(self, imageName, noiseType, noiseVal, brightType, brightValue, blurryType, blurryVal):
        df = DataFrame(
            {'IMAGE_NAME': imageName, 'NOISE_TYPE': noiseType, 'NOISY_VALUE': noiseVal, 'BRIGHT_TYPE': brightType,
             'BRIGHT_VALUE': brightValue, 'BLURRY_TYPE': blurryType, 'BLURRY_VALUE': blurryVal})

        return 0

    def writeData(self, fileName):
        f = open("ImageDetails.txt", "w+")
        f.write("This is line %d\r\n" % (1))
        f.close()
        return 0

    def image_cb(self, data):
        # global cv_image
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        self.main(cv_image)
        # image = np.array(Image.open(cv_image))
        # print(cv_image.type)
        # cv2.imshow("Image window", self.cv_image)
        # cv2.waitKey(3)

    def main(self, img):
        # img_dir = 'C:/Users/Michael/PycharmProjects/Camera_Aggregator/testbilder/'
        # datapath = os.path.join(img_dir, '*png')
        # files = glob.glob(datapath)
        data = []
        image_Name = []

        noisy_ImageType_List = []
        noise_Value_List = []

        fogy_Image_Type = []
        fog_Value_List = []

        bright_dark_ImageType_List = []
        bright_dark_Value_List = []

        blurry_sharp_ImageType_List = []
        blurry_sharp_Value_List = []


        image_Name = "img"
        data.append(img)
        grayImg = grayscale(img)

        # Calling Noise Estimation functionality
        algo = 1
        noise = noiseInImages(grayImg, algo)
        noise_Value_List.append(noise)
        noiseImageType1 = determineImageTypeBasedOnNoiseLevel(noise)
        noisy_ImageType_List.append(noiseImageType1)
        # End of Calling Noise Estimation functionality

        # Calling Fog Detection functionality
        im = imgpil.open(img).convert('L')
        print("==================PRINT=================")
        print(im)
        print("==================PRINT END=================")
        fogValue, fogMean, fogImgType = slow_horizontal_variance(im)
        fog_Value_List.append(fogValue)
        fogy_Image_Type.append(fogImgType)
        # End of Calling Fog Detection functionality

        # Calling Brightness Checker functionality
        brightnessType, brightnessMeanValue = hsvModel_brightness(img, "CameraPosition")
        bright_dark_ImageType_List.append(brightnessType)
        bright_dark_Value_List.append(brightnessMeanValue)
        # End of Calling Brightness Checker functionality

        # Calling Blurry Checker functionality
        blurryType, blurryValue = variance_of_laplacian(grayImg)
        blurry_sharp_ImageType_List.append(blurryType)
        blurry_sharp_Value_List.append(blurryValue)
        # End of Calling Blurry Checker functionality

        # self.writeImageDetails(image_Name,fogy_Image_Type,fog_Value_List,noisy_ImageType_List,noise_Value_List,bright_dark_ImageType_List,bright_dark_Value_List,blurry_sharp_ImageType_List,blurry_sharp_Value_List)
        self.writeImageDetails(image_Name, noisy_ImageType_List, noise_Value_List, bright_dark_ImageType_List,
                               bright_dark_Value_List, blurry_sharp_ImageType_List, blurry_sharp_Value_List)

        self.value.extend((noisy_ImageType_List, noise_Value_List, bright_dark_ImageType_List, bright_dark_Value_List,
                           blurry_sharp_ImageType_List, blurry_sharp_Value_List))

        for i, cx_rule in enumerate(self.tag_list):
            self.write_db(cx_rule, self.value[i])
        # key = cv2.waitKey(0)


if __name__ == "__main__":
    #try:
        image_processing()
   #except rospy.ROSInterruptException:
        #pass