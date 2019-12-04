import numpy as np
from PIL import ImageGrab
import cv2
import time
from directkeys import ReleaseKey, PressKey, W,A,S,D
d1 = 500
d2= 50
e1 =80
e2 = 200
a1=400
a2=400

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

def main():
     last_time = time.time()
     while True:
         screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
         new_screen, original_image = process_img(screen)
         #PressKey(W)
         #time.sleep(1)
         #ReleaseKey(W)
         #time.sleep(1)
         cv2.line(screen, (250, 500), (600,500), [100,0,100], 5)
         cv2.line(screen,(d1,d2), (600, 510),[200,50,200],5)
         cv2.line(screen,(e1,e2), (250,510),[100,45,150],5)
         cv2.line(screen,(a1,a2), (400,510),[100,45,150],5)
         r1=e1-250
         r2=e2-500
         s1=np.sqrt(r1**2+r2**2)
         cv2.putText(screen, "["+ str(s1)+"]", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
         f1=d1-600
         f2=d2-510
         s=np.sqrt(f1**2+f2**2)
         cv2.putText(screen, "["+ str(s)+"]", (400,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
         h1=d1-400
         h2=d2-510
         p=np.sqrt(h1**2+h2**2)
         cv2.putText(screen, "["+ str(p)+"]", (400,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)
          
         if p>20 and p<120:
              ReleaseKey(W)
              ReleaseKey(A)
              ReleaseKey(D)
              ReleaseKey(S)
         else: 
              if s>110 and s<200 and s1>110 and s1<200:
                   PressKey(W)
                   ReleaseKey(S)
                   ReleaseKey(A)
                   ReleaseKey(D)
         
              elif s1>100 and s>50 and s<100:
                   PressKey(A)
                   ReleaseKey(S)
                   ReleaseKey(D)
                   ReleaseKey(W)
              elif s>100 and s1>50 and s1<100:
                   PressKey(D)
                   ReleaseKey(S)
                   ReleaseKey(W)
                   ReleaseKey(A)
              else:
                   PressKey(S)
                   ReleaseKey(A)
                   ReleaseKey(W)
                   ReleaseKey(D)
         
         
         
         print('Loop took {} seconds'.format(time.time()-last_time))
         last_time = time.time()
         cv2.imshow('window', screen)
         
         #cv2.imshow('window2',cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
         #cv2.imshow('window',cv2.cvtColor(np.array(printscreen_pil), cv2.COLOR_BGR2RGB))
         if cv2.waitKey(25) and 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
main()
