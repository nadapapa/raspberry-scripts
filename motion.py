from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime
import RPi.GPIO as GPIO
import time
import sys
import subprocess

relay_pin = 17

GPIO.setmode(GPIO.BCM)

pir = MotionSensor(4)
camera = PiCamera()

camera.vflip = True
camera.hflip = True

GPIO.setwarnings(False)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.output(relay_pin, 1)

print("start")

try:
    while True:
        time.sleep(0.5)

        pir.wait_for_motion()
        print("motion")
        GPIO.output(relay_pin, 0)
        filename = "/home/pi/videos/" + datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
        camera.start_recording(filename)
           
        pir.wait_for_no_motion()
        print("no motion")
        GPIO.output(relay_pin, 1)
        camera.stop_recording()
        print("uploading to Dropbox")
        p = subprocess.Popen([sys.executable, 'dropboxUploader.py', filename],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        # dropboxUploader.dropboxUpload(filename)
        print("uploaded to Dropbox")
finally:
    camera.close()
    pir.close()
    GPIO.cleanup() # this ensures a clean exit