from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime
import RPi.GPIO as GPIO
import time

pir = MotionSensor(4)
camera = PiCamera()

camera.vflip = True
camera.hflip = True

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)

print("start")

try:
    while True:
        time.sleep(0.5)
        pir.wait_for_motion()
        print("motion")
        GPIO.output(17, 1)
        filename = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")    
        camera.start_recording("/home/pi/videos/" + filename)
           
        pir.wait_for_no_motion()
        print("no motion")
        GPIO.output(17, 0)
        camera.stop_recording()

except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
    GPIO.cleanup()
    camera.close()
