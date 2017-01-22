from gpiozero import MotionSensor
from gpiozero import LED
from picamera import PiCamera
from datetime import datetime
import time

pir = MotionSensor(4)
led = LED(17)
camera = PiCamera()

while True:
    time.sleep(0.5)
    pir.wait_for_motion()
    print("motion")
    led.on()
    filename = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")    
    camera.start_recording("/home/pi/videos/" + filename)
    
    pir.wait_for_no_motion()
    print("no motion")
    camera.stop_recording()
    led.off()
