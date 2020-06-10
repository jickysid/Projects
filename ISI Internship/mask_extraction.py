#CREATING MASKS AND SAVING THEM TO A FOLDER

import os
import cv2
import numpy as np

def get_mask(cap,filename):
    #cv2.imshow(cap)
    hsv = cv2.cvtColor(cap, cv2.COLOR_BGR2HSV)
    #person
    array1 = np.array([0,85,192]) #extract these values using isi_mask code for each class
    mask1 = cv2.inRange(hsv, array1, array1)
    res1 = cv2.bitwise_and(cap,cap, mask = mask1)
    res1 = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
    ret, res1 = cv2.threshold(res1,35,255,cv2.THRESH_BINARY) #create a binary image
    xyz = filename[:-4] + "1" + ".png" #xyz is output filename and "1" represents the class 1
    cv2.imwrite('C:/Users/user/Desktop/ZN/ISI/VOC2012/Segmentation_MaskB/' + xyz,res1)#saving the image to a folder
    #aeroplane
    array2 = np.array([0,255,128])
    mask2 = cv2.inRange(hsv, array2, array2)
    res2 = cv2.bitwise_and(cap,cap, mask = mask2)
    res2 = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)
    ret, res2 = cv2.threshold(res2,35,255,cv2.THRESH_BINARY)
    xyz = filename[:-4] + "2" + ".png"
    cv2.imwrite('C:/Users/user/Desktop/ZN/ISI/VOC2012/Segmentation_MaskB/' + xyz,res2)
    #bottle
    array3 = np.array([150,255,128])
    mask3 = cv2.inRange(hsv, array3, array3)
    res3 = cv2.bitwise_and(cap,cap, mask = mask3)
    res3 = cv2.cvtColor(res3, cv2.COLOR_BGR2GRAY)
    ret, res3 = cv2.threshold(res3,35,255,cv2.THRESH_BINARY)
    xyz = filename[:-4] + "3" + ".png"
    cv2.imwrite('C:/Users/user/Desktop/ZN/ISI/VOC2012/Segmentation_MaskB/' + xyz,res3)
    #table
    array4 = np.array([20,255,192])
    mask4 = cv2.inRange(hsv, array4, array4)
    res4 = cv2.bitwise_and(cap,cap, mask = mask4)
    res4 = cv2.cvtColor(res4, cv2.COLOR_BGR2GRAY)
    ret, res4 = cv2.threshold(res4,35,255,cv2.THRESH_BINARY)
    xyz = filename[:-4] + "4" + ".png"
    cv2.imwrite('C:/Users/user/Desktop/ZN/ISI/VOC2012/Segmentation_MaskB/' + xyz,res4)
    #bus and train
    array5 = np.array([90,255,128])
    mask5 = cv2.inRange(hsv, array5, array5)
    array6 = np.array([40,255,192])
    mask6 = cv2.inRange(hsv, array6, array6)
    mask = cv2.bitwise_or(mask5, mask6)
    res5 = cv2.bitwise_and(cap,cap, mask = mask)
    res5 = cv2.cvtColor(res5, cv2.COLOR_BGR2GRAY)
    ret, res5 = cv2.threshold(res5,5,255,cv2.THRESH_BINARY)
    xyz = filename[:-4] + "5" + ".png"
    cv2.imwrite('C:/Users/user/Desktop/ZN/ISI/VOC2012/Segmentation_MaskB(2)/' + xyz,res5)
    #cat
    array6 = np.array([40,255,192])
    mask6 = cv2.inRange(hsv, array6, array6)
    res6 = cv2.bitwise_and(cap,cap, mask = mask6) 
    res6 = cv2.cvtColor(res6, cv2.COLOR_BGR2GRAY)
    ret, res6 = cv2.threshold(res6,35,255,cv2.THRESH_BINARY)
    xyz = filename[:-4] + "6" + ".png"
    #cv2_imshow(res2)
    cv2.imwrite('C:/Users/user/Desktop/ZN/ISI/VOC2012/Segmentation_MaskB/' + xyz,res6)

#    return res1,res2,res3,res4,res5,res6

for filename in os.listdir("C:/Users/user/Desktop/ZN/ISI/VOC2012/SegmentationClass"):# list the names of images from the folder containing ground truths
    src =os.path.join('C:/Users/user/Desktop/ZN/ISI/VOC2012/SegmentationClass', filename)
    print "loop"
    cap = cv2.imread(src,1)
    cap = cv2.resize(cap, (224,224))
    #print cap.shape
    get_mask(cap,filename)
    
