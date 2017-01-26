from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime
import RPi.GPIO as GPIO
import time

relay_pin = 17

pir = MotionSensor(4)
camera = PiCamera()

camera.vflip = True
camera.hflip = True

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.output(relay_pin, 1)

print("start")

def motion():
    print("motion")
    GPIO.output(relay_pin, 0)
    filename = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
    camera.start_recording("/home/pi/videos/" + filename)

def noMotion():
    print("no motion")
    GPIO.output(relay_pin, 1)
    camera.stop_recording()



try:
    while True:
        time.sleep(0.5)

        pir.wait_for_motion()
        motion()
           
        pir.wait_for_no_motion()
        noMotion()


except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
    camera.close()
    GPIO.cleanup()