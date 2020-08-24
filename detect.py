import numpy as np
import cv2
import RPi.GPIO as GPIO
import time

motorRotation = 0 # middle
max_motor_rotation = 70

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
enable_pin=18
coil_A_1_pin = 4 # blue
coil_A_2_pin = 17 # yellow
coil_B_1_pin = 23 # green
coil_B_2_pin = 24 # gray
 
# adjust if different
StepCount = 8
Seq = list(range(0, StepCount))
Seq[0] = [1,0,0,0]
Seq[1] = [1,1,0,0]
Seq[2] = [0,1,0,0]
Seq[3] = [0,1,1,0]
Seq[4] = [0,0,1,0]
Seq[5] = [0,0,1,1]
Seq[6] = [0,0,0,1]
Seq[7] = [1,0,0,1]
 
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
 
GPIO.output(enable_pin, 1)

 
if __name__ == '__main__':
    faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,     
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20)
        )
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            
            # motor movement
            if ((x+(w/2)) > 320):
                calculatedRotation = int((((x+(w/2)) - 320) / 320) * max_motor_rotation)
                if (motorRotation - calculatedRotation > -max_motor_rotation):
                    #backwards(5 / 1000.0, calculatedRotation)
                    for i in range(calculatedRotation):
                        for j in reversed(range(StepCount)):
                            GPIO.output(coil_A_1_pin, Seq[j][0])
                            GPIO.output(coil_A_2_pin, Seq[j][1])
                            GPIO.output(coil_B_1_pin, Seq[j][2])
                            GPIO.output(coil_B_2_pin, Seq[j][3])
                            time.sleep(5 / 1000.0)
                    motorRotation = motorRotation - calculatedRotation
            else:
                calculatedRotation = int(((x+(w/2)) / 320) * max_motor_rotation)
                if (motorRotation + calculatedRotation < max_motor_rotation):
                    for i in range(calculatedRotation):
                        for j in range(StepCount):
                            GPIO.output(coil_A_1_pin, Seq[j][0])
                            GPIO.output(coil_A_2_pin, Seq[j][1])
                            GPIO.output(coil_B_1_pin, Seq[j][2])
                            GPIO.output(coil_B_2_pin, Seq[j][3])
                            time.sleep(5 / 1000.0)
                    motorRotation = motorRotation + calculatedRotation
            
        if (len(faces) == 0):
            if (motorRotation) < 0:
                for i in range(abs(motorRotation)):
                    for j in range(StepCount):
                        GPIO.output(coil_A_1_pin, Seq[j][0])
                        GPIO.output(coil_A_2_pin, Seq[j][1])
                        GPIO.output(coil_B_1_pin, Seq[j][2])
                        GPIO.output(coil_B_2_pin, Seq[j][3])
                        time.sleep(5 / 1000.0)
                motorRotation = 0
            else:
                for i in range(motorRotation):
                    for j in reversed(range(StepCount)):
                        GPIO.output(coil_A_1_pin, Seq[j][0])
                        GPIO.output(coil_A_2_pin, Seq[j][1])
                        GPIO.output(coil_B_1_pin, Seq[j][2])
                        GPIO.output(coil_B_2_pin, Seq[j][3])
                        time.sleep(5 / 1000.0)
                motorRotation = 0
                
                    
        cv2.imshow('video',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break
    cap.release()
    cv2.destroyAllWindows()

    
