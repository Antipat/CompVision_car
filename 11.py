import RPi.GPIO as GPIO  #импорт библиотеки
import time

GPIO.setmode(GPIO.BOARD) #"включение" GPIO

GPIO.setup(35, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)

GPIO.output(40, 1)
GPIO.output(33, 1)
while True:
    GPIO.output(35, 1)
    
    GPIO.output(37, 0)
    
    GPIO.output(36, 1)
  
    GPIO.output(38, 0)
    time.sleep(1)

    GPIO.output(35, 0)
    
    GPIO.output(37, 1)
    
    GPIO.output(36, 0)
    
    GPIO.output(38, 1)
    time.sleep(1)

    GPIO.output(35, 0)
    
    GPIO.output(37, 1)
    
    GPIO.output(36, 1)
    
    GPIO.output(38, 0)
    time.sleep(1)

    GPIO.output(35, 1)
    
    GPIO.output(37, 0)
    
    GPIO.output(36, 0)
    
    GPIO.output(38, 1)
    time.sleep(1)




    
