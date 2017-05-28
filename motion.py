#!/usr/bin/env python3

from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime
import RPi.GPIO as GPIO
import time
import sys
import subprocess

relay_pin = 17
raw_video_extension = '.h264'
converted_video_extension = '.mp4'

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
        time.sleep(1);
        now_time = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        filename = "/home/pi/videos/" + now_time
        camera.capture("/home/pi/motion.jpg")
        p = subprocess.Popen(["mpack", "-s", "motion detected", "/home/pi/motion.jpg", "nadapapa@gmail.com"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        camera.start_recording(filename + raw_video_extension)

        pir.wait_for_no_motion()
        print("no motion")
        GPIO.output(relay_pin, 1)
        camera.stop_recording()

        print("converting to mp4")
        p = subprocess.Popen(['MP4Box', '-add', filename + raw_video_extension, filename + converted_video_extension],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        p.wait()

        print("uploading to Dropbox")
        log = open('/tmp/log2', 'w')
        p = subprocess.Popen(['/home/pi/raspberry-scripts/dropboxUploader.py', filename + converted_video_extension],
                           stdout=log,
                           stderr=subprocess.STDOUT)
finally:
    camera.close()
    pir.close()
    GPIO.cleanup() # this ensures a clean exit
