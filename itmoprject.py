import time
import math
import cv2
import keyboard
import serial
backSub_mog = cv2.createBackgroundSubtractorMOG2()
arduino_port = '/dev/ttyUSB0'
imgpath = "arm.jpg"

c = True
ser = serial.Serial(arduino_port, baud_rate)
while c ==True:
    if keyboard.is_pressed("space"):
        c = False
    # read image
    img = cv2.imread(imgpath)
    img = cv2.resize(img, (320, 240))
    img = cv2.GaussianBlur(img, (9, 9), 0)
    imgNoBg =  backSub_mog.apply(img)
    side = 500
    # show both images
    imgNoBg =cv2.resize(imgNoBg,(1000, 1000))
    img =cv2.resize(img,(1000,1000))
    contours, hierarchy = cv2.findContours(imgNoBg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        if area>20000:
         cv2.line(img, (0, 500), (x+w, y), (0, 0, 255), thickness=3)
         cv2.line(img, (0, 1000), (x + w, 1000), (0, 0, 255), thickness=3)
         w1 = str(x+w)
         cv2.putText(img, "width:" + " " + w1, (100, 100), cv2.FONT_HERSHEY_TRIPLEX, 3, (0, 0, 255), 3)
         d = w1
         hight = (1000-y)
         h1 = str(hight)
         cv2.putText(img, "hight:" + " " + h1, (100, 400), cv2.FONT_HERSHEY_TRIPLEX, 3, (0, 0, 255), 3)
         pi = math.pi
         alpha = 180 - (math.atan((x+w-300)/(700-y)))*180/pi
         beta =  180 - (math.atan((700-y)/(x+w-300)))*180/pi
         cv2.putText(img, "alpha:" + " " + str(alpha), (100, 700), cv2.FONT_HERSHEY_TRIPLEX, 3, (0, 0, 255), 3)
         cv2.putText(img, "beta:" + " " + str(beta), (100, 600), cv2.FONT_HERSHEY_TRIPLEX, 3, (0, 0, 255), 3)
         data_to_send = alpha
         ser.write((data_to_send + '\n').encode('utf-8'))
         time.sleep(1)
         a = ser.readline().decode('utf-8').rstrip()
         a = int(a)
         while a!=1:
             time.sleep(1)
         data_to_send = beta
         ser.write((data_to_send + '\n').encode('utf-8'))
         time.sleep(1)
    cv2.imshow('result', img)
    cv2.waitKey(1)
cv2.destroyAllWindows()
print(img.shape)