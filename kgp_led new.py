import numpy as np
import cv2
import math
import serial
import time

   
def nothing(x):
    pass
cap = cv2.VideoCapture(1)
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.namedWindow('BW', cv2.WINDOW_NORMAL)
cv2.createTrackbar('L', 'Image', 0, 255, nothing)
cv2.createTrackbar('H', 'Image', 0, 255, nothing)
cv2.createTrackbar('T', 'BW', 0, 255, nothing)
ser = serial.Serial('COM14',2400)
leftturn = 0
rightturn = 0
led = 0
cntr = 0


while(True):
    ret, frame = cap.read()
    
    if ret == True:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([179, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)

##        hsv_1 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
##        lower_blue = np.array([84,21,219])
##        upper_blue = np.array([140,188,255])
##        mask_1 = cv2.inRange(hsv_1, lower_blue, upper_blue)
        roi_1 = mask[0:200,0:640]
        result = cv2.bitwise_and(frame, frame, mask=mask)
        #cv2.imshow('LED',roi_1)
        pixels = cv2.findNonZero(roi_1)
        
        if pixels is not None:
            print len(pixels)
            #th = cv2.getTrackbarPos('T', 'LED')
            if len(pixels) > 500:
                led = led + 1
                cntr = 12
            elif len(pixels)> 300 :
                led = led + 1
                print len(pixels)
        if led > 0:
            cntr = cntr + 1
            print 'LED_AILA'
            
            
             
        print led, cntr
        if cntr > 20:                       # 33 for straight, 10 for left turn\
            ser.write('b')
            print 'AEITHI ACHHI LED'
            cntr = 0
            led = 0
            time.sleep(3.5)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        th = cv2.getTrackbarPos('T', 'BW')
        ret,thl = cv2.threshold(gray,95,255,cv2.THRESH_BINARY)
        cv2.imshow('BW',thl)
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(thl, cv2.MORPH_OPEN, kernel)
        minm = cv2.getTrackbarPos('L', 'Image')
        maxm = cv2.getTrackbarPos('H', 'Image')
        edge = cv2.Canny(thl,minm,maxm)
        lines = cv2.HoughLinesP(edge,1,np.pi/180,25,minLineLength=10,maxLineGap=300)
            
        #find solution for no lines
        error = 0
        leftAng = 0
        rightAng = 0
        leftN = 0
        rightN = 0
        leftLenSum = 0
        rightLenSum = 0
        FinLeftAng = 0
        FinRightAng = 0
        FinLeftLen = 0
        FinRightLen = 0
        ytot = 0
        yno = 0
        if lines is not None:
            for x1,y1,x2,y2 in lines[0]: 
                cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
                if x1==x2:
                    continue
                    angle = 90.00
                else:
                    slope = float((y2-y1))/float((x2-x1))
                    intercept = float(y1 - slope*x1)
                    angle = math.degrees(math.atan(slope))
                    #print 'Angle:'
                    #print angle
                    if abs(angle) < 12:
                        angle = 0
                    elif angle>70:
                        leftturn = 1
                        rightturn = 0
                        angle = 0
                        rightLen = 0
                        #print 'leftturn'
                    elif angle < -70:
                        rightturn = 1
                        leftturn = 0
                        angle = 0
                        leftLen = 0
                        #print 'rightturn'
                    elif angle>0:
                        rightLen = np.sqrt((y2-y1)**2+(x2-x1)**2)
                        rightLenSum = rightLenSum + rightLen 
                        rightAng = rightAng + angle
                        rightN = rightN + 1
                        #b=1
                    elif angle<0:
                        leftLen = np.sqrt((y2-y1)**2+(x2-x1)**2)
                        leftLenSum = leftLenSum + leftLen
                        leftAng = leftAng +angle
                        leftN = leftN + 1
                        #c=1
                        
                        
                #print slope, angle
                    
        if leftN !=0 :
            FinLeftAng = float(leftAng)/float(leftN)
            FinLeftLen = float(leftLenSum)/float(leftN)
            
        if rightN !=0 :
            FinRightAng = float(rightAng)/float(rightN)
            FinRightLen = float(rightLenSum)/float(rightN)
        error = FinLeftAng + FinRightAng
        #no = a+b+c
        print error,FinLeftAng,FinRightAng

        if error == 0:
            if lines is not None:
                for x1,y1,x2,y2 in lines[0]:
                    ytot = ytot+y2+y1
                    yno = yno+2
                yavg = float(ytot)/float(yno)
                print(yavg)
                if yavg>290:
                    if leftturn == 1:
                        print 'B'
                        ser.write('B')
                        time.sleep(0.2)
                        ser.write('q')
                        time.sleep(0.5)
                        ser.write('x')
                        print 'LT'
                        time.sleep(0.75)
                        ser.write('S')
                        #time.sleep(0.2)
                        ser.write('B')
                        time.sleep(0.2)
                        leftturn = 0
                        
                    elif rightturn == 1:
                        print 'B'
                        ser.write('B')
                        time.sleep(0.2)
                        ser.write('p')
                        time.sleep(0.5)
                        ser.write('y')
                        print 'RT'
                        time.sleep(0.6)
                        ser.write('S')
                        #time.sleep(0.2)
                        ser.write('B')
                        time.sleep(0.2)
                        #ser.write('q')
                        rightturn=0
                        
##                    else :
##                        time.sleep(0.25)
##                        ser.write('S')
##                        print 'Sari Gala Track'
##                        break
##                        
                else:
                    print 'F'
                    ser.write('F')
    
        elif abs(error)<10:
            if FinLeftLen < FinRightLen:
                print 'FL'
                ser.write('l')
                #time.sleep(0.2)
            elif FinRightLen < FinLeftLen:
                print 'FR'
                ser.write('r')
                #time.sleep(0.2)
        elif abs(error)>10 and abs(error)<20  :
            if FinLeftLen < FinRightLen:
                print 'ML'
                ser.write('p')
                #time.sleep(0.2)
            elif FinRightLen < FinLeftLen:
                print 'MR'
                ser.write('q')
                #time.sleep(0.2)
        elif error < 0:
            print 'R'
            ser.write('R')
            #time.sleep(0.2)
        elif error > 0:
            print 'L'
            ser.write('L')
            #time.sleep(0.2)
        
        
        #x=ser.readline()
        #print x
        #cv2.imshow('Image',edge)
        cv2.imshow('lines',frame)
        if cv2.waitKey(30) ==ord('q'):
            if lines is not None:
                print lines[0]
                for x1,y1,x2,y2 in lines[0]:
                    print np.sqrt((y2-y1)**2+(x2-x1)**2)
            ser.write('S')
            break
        else:
            continue                                                                    
    else:
        continue
cap.release()
cv2.destroyAllWindows()
