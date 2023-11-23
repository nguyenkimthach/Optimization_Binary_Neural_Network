import tensorflow as tf
from tensorflow import keras
import larq as lq
import numpy as np
import cv2
from picamera2 import Picamera2, Preview
from keras.models import load_model
import lcddriver
import time
import matplotlib.pyplot as plt
import pyrebase
import RPi.GPIO as GPIO
print("finish Import Library")
############################

config = {
  "apiKey": "4j74F3rmDObWUUcxvAyKwL5IyAg9oSpWuYueBQgQ",
  "authDomain": "raspberry-pizero-2w-ccnp-de430.firebaseapp.com",
  "databaseURL": "https://raspberry-pizero-2w-ccnp-de430-default-rtdb.firebaseio.com",
  "storageBucket": "raspberry-pizero-2w-ccnp-de430.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

display = lcddriver.lcd()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

sensor = 24
GPIO.setup(sensor,GPIO.IN)

buzzer=17
GPIO.setup(buzzer,GPIO.OUT)

print("dang nap chuong trinh")
display.lcd_display_string("Load Data...",1)
display.lcd_display_string("Wait a minute", 2)
##########################

#check send data to firebase
checkNG = 63
data = {
        "machine 1": checkNG,
        }
db.child("machine").set(data)
display.lcd_clear()
print("Send database ok")
display.lcd_display_string("test Database OK",1)
##########################

#Set value to change binary Image
img_width, img_height= 100, 100
img_thresh =90
def convert_to_binary(img_grayscale, thresh=100):
    thresh, img_binary = cv2.threshold(img_grayscale, thresh, maxval=255, type=cv2.THRESH_BINARY)
    return img_binary
############################

#Load model
model = keras.models.load_model('Model_CCNPdataset_BCNN_32bach_100eb_8163264285612.h5')
print("load model ok")

#change image to binay image
img = cv2.imread('/home/thach/image_1.jpg',0)
img = convert_to_binary(img, thresh= img_thresh)
img = cv2.resize(img, (img_width, img_height))
img = cv2.bitwise_not(img)
img = img.reshape(1, img_width, img_height, 1)
    
#check predict image   
result = model.predict(img)
print("predict1 test ok")

display.lcd_display_string("Predict test OK",2)
time.sleep(2)
############################

display.lcd_clear()
print("Finished Load")
display.lcd_display_string("Finished Load...",1)

lis = ['NC F06', 'NC K11', 'NC S19', 'NC V22']

picam = Picamera2()
config = picam.create_preview_configuration()
picam.configure(config)
picam.start_preview(False)
picam.start()
############################

#for i in range(50):
while(1):
    if(GPIO.input(sensor) == False):
        print("dang xac nhan")
        
        GPIO.output(buzzer,GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(buzzer,GPIO.LOW)
        
        display.lcd_clear()
        display.lcd_display_string("confirming...",1)
        display.lcd_display_string("Wait a minute", 2)
        
        picam.capture_file('/home/thach/image_1.jpg')
        #time.sleep(10)
        
        img = cv2.imread('/home/thach/image_1.jpg',0)
        img = convert_to_binary(img, thresh= img_thresh)
        img = cv2.resize(img, (img_width, img_height))
        img = cv2.bitwise_not(img)
        img = img.reshape(1, img_width, img_height, 1)
        #plt.imshow(img,cmap='gray')
        #plt.show()
        
        print("dang tinh toan")
        display.lcd_clear()
        display.lcd_display_string("calculating...", 1)
        display.lcd_display_string("Wait a minute", 2)
        
        start_time = time.time()
        
        result = model.predict(img) #predict img
        print("execution time:  %s ms" % ((time.time() - start_time)*1000/1)) #caculate predict time

        max= np.argmax(result)
        print('Đây là lot: ',lis[max]) #Print lot
        
        
        #Print Lot
        display.lcd_clear()
        display.lcd_display_string("time is: " + str((time.time() - start_time)*1000/1),1)
        display.lcd_display_string("Lot is: "+ lis[np.argmax(result)] , 2)
        
        #check NG Lot
        if(max < 2): 
            checkNG = 0
            display.lcd_display_string("OK Lot: ",2)
            print('OK lot: ',lis[max]) #Print OK lot
        else:
            checkNG = 1
            display.lcd_display_string("NG Lot: ",2)
            print('NG Lot: ',lis[max]) #Print NG lot

        data = {
            "machine 1": checkNG,
            }
        db.child("machine").set(data)
        print("finish Send Data to Firebase")
        
        if(checkNG == 0): 
            time.sleep(2)
        else:
            for i in range(3):
                GPIO.output(buzzer,GPIO.HIGH)
                print ("Beep")
                time.sleep(0.5)
                GPIO.output(buzzer,GPIO.LOW)
                print ("No Beep")
                time.sleep(0.5)
    else:
        print("Chưa co thung san pham")
        display.lcd_clear()
        display.lcd_display_string("**** NO BOX ****",1)
        while GPIO.input(sensor):
           time.sleep(0.2) 



############################
picam.close()

