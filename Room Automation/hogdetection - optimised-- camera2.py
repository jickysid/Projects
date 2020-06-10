from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import socket

cam = cv2.VideoCapture(0)
#cam.open(0)
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cy1 = float(0)

#Creates instance of 'Socket'
s = socket.socket()

hostname = '192.168.43.148' #Server IP/Hostname
port = 8000 #Server Port

s.connect((hostname,port)) #Connects to server

while True:
    
  #  image = cv2.imread("C:/Users/dell/Desktop/a.jpg")
    ret ,image = cam.read()
    if ret == True:
        image = imutils.resize(image, width=min(400, image.shape[1]))
        orig = image.copy()
     
            # detect people in the image
        (rects, weights) = hog.detectMultiScale(image, winStride=(4,4),padding=( 10 ,10), scale=1.05)
     
            # draw the original bounding boxes
        for (x, y, w, h) in rects:
            cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
           # print ((x+x+w)/2)
     
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=12.95)
     
            # draw the final bounding boxes
        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
                # show the output images
            #print (xA, xB, yA, yB)
            cy1 = float(400) - float((xA+xB)/2)        #shifting of origin for camera 2
            cx1 = float((yA+yB)/2)
            print (cy1)

        cv2.imshow("output", image)

        b1=float(375.5)             #view angle distance
        b2= float(300)
        m1=float(150)               #distance of camera from origin
        m2=float(200)
        a1 = float(cy1-m1)          #distance of projection from camera
        print (a1)                  #feed to other camera
        
        
        #x = raw_input("Enter message: ") #Gets the message to be sent
        s.send(str(a1).encode()) #Encodes and sends message (x)
        message = s.recv(1024).decode() #Gets the incomming message
        print("Message is",message)
       
        a2 = float(message)

        X=(((a1*m2)+(m1*b1))*b2)/((b1*b2)-(a1*a2))          #formula for actual coordinates
        Y=(b1*(X-m1))/(a1)
        print (X,Y)
    else:
        continue

    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break
        
cam.release()
cv2.destroyAllWindows()
