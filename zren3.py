import io
import picamera
import cv2
import numpy as np
import time
import RPi.GPIO as GPIO  #импорт библиотеки
d1 = 500
d2= 50
e1 =80
e2 = 200
a1=400
a2=400
t1=0
GPIO.setmode(GPIO.BOARD) #"включение" GPIO

GPIO.setup(35, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)

GPIO.output(40, 1)
GPIO.output(33, 1)
def draw_lines(image, lines):
     global d1, d2
     try:
          for line in lines:
               coords=line[0]
               cv2.line(image, (coords[0], coords[1]), (coords[2], coords[3]), [0,255,2], 5)
               d1=lines[0][0][0]
               d2=lines[0][0][1]
     except:
          pass
     
def draw_lines1(image, lines1):
     global e1,e2
     try:
          for line in lines1:
               coords=line[0]
               cv2.line(image, (coords[0], coords[1]), (coords[2], coords[3]), [0,255,2], 5)
               
               e1 = lines1[0][0][0]
               e2 = lines1[0][0][1]
     except:
          pass
def draw_lines3(image, lines3):
     global a1, a2
     try:
          for line in lines3:
               coords=line[0]
               cv2.line(image, (coords[0], coords[1]), (coords[2], coords[3]), [0,255,100], 5)
               a1=lines3[0][0][0]
               a2=lines3[0][0][1]
     except:
          pass
     
def roi (image, vertics):
     mask = np.zeros_like(image)
     cv2.fillPoly(mask, vertics,255)
     masked = cv2.bitwise_and(image, mask)
     return masked

def process_img(image):
     global d1,d2, e1, e2, a1, a2
     original_image = image 
     processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
     processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
     vertics = np.array([[50,500], [10,300], [210,350], [420,350], [640,300], [800,500]])
     vertics1 = np.array([[530,450], [530,300], [800,300], [800,450]])
     vertics2 = np.array([[110,500], [110,300], [200,300], [200,300]])
     vertics3 = np.array([[360,400], [360,500], [450,400], [450,500]])

                           
     processed_img = roi(processed_img, [vertics])
     processed_img1 = roi(processed_img, [vertics1])
     processed_img2 = roi(processed_img, [vertics2])
     processed_img3 = roi(processed_img, [vertics3])
     lines = cv2.HoughLinesP(processed_img1, 1, np.pi/180,10,50,5)
     lines1 = cv2.HoughLinesP(processed_img2, 1, np.pi/180,10,50,1)
     lines3 = cv2.HoughLinesP(processed_img3, 1, np.pi/180,10,50,5)
                         
     draw_lines(processed_img1, lines)
     draw_lines(image,lines)

     draw_lines1(processed_img2, lines1)
     draw_lines1(image,lines1)

     draw_lines3(processed_img3, lines3)
     draw_lines3(image,lines3)
     
     #d1=lines[0][0][0]
     #d2=lines[0][0][1]

     #e1=lines1[0][0][0]
     #e2=lines1[0][0][1]
     
     
     return processed_img, original_image

    
#t = io.BytesIO()
#ret, frame = cap.read()
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('Woutput181.mp4', fourcc, 20.0, (640,480))

def main():
     global t1
     last_time = time.time()
     t = io.BytesIO()
     time.sleep(0.3)
     with picamera.PiCamera() as camera:
         
         camera.resolution = (720, 640)
         cap=camera.capture(t, format='png')
         
         

    #camera.start_preview()
    
     buff = np.fromstring(t.getvalue(), dtype=np.uint8)
     image1 = cv2.imdecode(buff, 1)
     gray = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY)
     lower_red = np.array([0,180,200])
     upper_red = np.array([255,225,225])
    
     #res1 = cv2.matchTemplate(gray,template,3)
     #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res1)
     while True:
         #screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
         new_screen, original_image = process_img(image1)
         #PressKey(W)
         #time.sleep(1)
         #ReleaseKey(W)
         #time.sleep(1)
         cv2.line(image1, (250, 500), (600,500), [100,0,100], 5)
         cv2.line(image1,(d1,d2), (600, 510),[200,50,200],5)
         cv2.line(image1,(e1,e2), (250,510),[100,45,150],5)
         cv2.line(image1,(a1,a2), (400,510),[100,45,150],5)
         r1=e1-250
         r2=e2-500
         s1=np.sqrt(r1**2+r2**2)
         cv2.putText(image1, "["+ str(s1)+"]", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
         f1=d1-600
         f2=d2-510
         s=np.sqrt(f1**2+f2**2)
         cv2.putText(image1, "["+ str(s)+"]", (400,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
         h1=d1-400
         h2=d2-510
         p=np.sqrt(h1**2+h2**2)
         cv2.putText(image1, "["+ str(p)+"]", (400,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
          
         if p>50 and p<400:
             GPIO.output(35, 0)
    
             GPIO.output(37, 0)
    
             GPIO.output(36, 0)
  
             GPIO.output(38, 0)
         
             
         #else :
         if s>110 and s<200 and s1>110 and s1<200:
              GPIO.output(35, 1)

              GPIO.output(37, 0)
    
              GPIO.output(36, 1)
   
              GPIO.output(38, 0)
         
         elif s1>200 and s>50 and s<140:
                  
              GPIO.output(35, 0)
    
              GPIO.output(37, 1)
    
              GPIO.output(36, 1)
  
              GPIO.output(38, 0)
                   
         elif s>200 and s1>50 and s1<200:
              GPIO.output(35, 1)
    
              GPIO.output(37, 0)
    
              GPIO.output(36, 0)
  
              GPIO.output(38, 1)
                  
         else:
              GPIO.output(35, 0)
    
              GPIO.output(37, 0)
    
              GPIO.output(36, 0)
  
              GPIO.output(38, 0)
         
         
         
         print('Loop took {} seconds'.format(time.time()-last_time))
         last_time = time.time()
         #cv2.imshow('window', image1)
         kk=str(t1)
         ss=kk+'.jpg'
         cv2.imwrite(ss,image1)
         t1=t1+10
         
         

while True:                    
     main()


    #cv2.imshow('frame', gray)
    #out.write(gray)
#cv2.imwrite('result.jpg',image)
#cv2.destroyAllWindows()
#cap.release()
