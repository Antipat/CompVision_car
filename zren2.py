import io
import picamera
import cv2
import numpy as np
import time
import RPi.GPIO as GPIO  #импорт библиотеки

GPIO.setmode(GPIO.BOARD) #"включение" GPIO

GPIO.setup(35, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)

GPIO.output(40, 1)
GPIO.output(33, 1)

#t = io.BytesIO()
#ret, frame = cap.read()
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('Woutput181.mp4', fourcc, 20.0, (640,480))
template = cv2.imread("self15.png",0)
w, h = template.shape[::-1]
x,y = 0,0
while True:
    t = io.BytesIO()
    time.sleep(0.3)
    with picamera.PiCamera() as camera:
        camera.resolution = (720, 640)
        cap=camera.capture(t, format='jpeg')

    #camera.start_preview()
    
    buff = np.fromstring(t.getvalue(), dtype=np.uint8)
    image = cv2.imdecode(buff, 1)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    lower_red = np.array([0,180,200])
    upper_red = np.array([255,225,225])
    
    res1 = cv2.matchTemplate(gray,template,3)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res1)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    x = (top_left[0] + bottom_right[0])/2
    y = (top_left[1] + bottom_right[1])/2
    if y>200 and y<500:
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 3)
        cv2.putText(image, "["+ str(x)+","+str(y)+"]", (bottom_right[0]+10,bottom_right[1]+10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
        GPIO.output(35, 0)
    
        GPIO.output(37, 1)
    
        GPIO.output(36, 0)
  
        GPIO.output(38, 1)
        #time.sleep(1)
    else:
        GPIO.output(35, 1)
    
        GPIO.output(37, 0)
    
        GPIO.output(36, 1)
    
        GPIO.output(38, 0)
    #cv2.imshow('frame', gray)
    #out.write(gray)
    cv2.imwrite('result.jpg',image)
cv2.destroyAllWindows()
cap.release()
