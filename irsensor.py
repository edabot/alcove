import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23,GPIO.IN)

try:
    time.sleep(2)
    while True:
        if GPIO.input(23):
            print('Motion detected')
            time.sleep(1)
        time.sleep(0.1)
except:
    GPIO.cleanup()