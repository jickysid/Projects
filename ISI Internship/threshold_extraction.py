import numpy as np
import cv2
def nothing(x):
    pass
#cap = cv2.VideoCapture(0)
cap = cv2.imread('C:\Users\user\Desktop\ZN\PYTHON\pascal voc\2007_000876',1)
cv2.namedWindow('OBJECT', cv2.WINDOW_NORMAL)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.createTrackbar('min_h', 'image', 56, 179, nothing)
cv2.createTrackbar('max_h', 'image', 90, 179, nothing)
cv2.createTrackbar('min_s', 'image', 121, 255, nothing)
cv2.createTrackbar('max_s', 'image', 255, 255, nothing)
cv2.createTrackbar('min_v', 'image', 134, 255, nothing)
cv2.createTrackbar('max_v', 'image', 255, 255, nothing)
while(True):
    ret, frame = cap.read()
    #print frame.shape
    
    if ret == True:
        cv2.imshow('image', frame)

        
        #L = cv2.getTrackbarPos('L', 'OBJECT')
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
        min_h = cv2.getTrackbarPos('min_h', 'image')
        max_h = cv2.getTrackbarPos('max_h', 'image')
        min_s = cv2.getTrackbarPos('min_s', 'image')
        max_s = cv2.getTrackbarPos('max_s', 'image')
        min_v = cv2.getTrackbarPos('min_v', 'image')
        max_v = cv2.getTrackbarPos('max_v', 'image')
        lower_green = np.array([min_h,min_s,min_v])
        upper_green = np.array([max_h,max_s, max_v])
        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask = cv2.blur(mask, (3,3))
        print(mask.shape)
        cv2.imshow('OBJECT',mask)
        #ret,thresh = cv2.threshold(mask,41,255,cv2.THRESH_BINARY)
        edge = cv2.Canny(mask,50,150)
        #cv2.imshow('thresh', thresh)
        cv2.imshow('edge',edge)

    else:
        continue
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
