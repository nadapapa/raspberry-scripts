from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime
import RPi.GPIO as GPIO
import dropbox
import time
import os
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

app_key = config["DROPBOX"]["app_key"]
app_secret = config["DROPBOX"]["app_secret"]
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

def dropboxAuth():
    accessTokenFileOverwrite = open("accessToken.txt", "w+")

    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

    # Have the user sign in and authorize this token
    authorize_url = flow.start()
    print('1. Go to: ' + authorize_url)
    print('2. Click "Allow" (you might have to log in first)')
    print('3. Copy the authorization code.')
    code = input("Enter the authorization code here: ").strip()

    try:
        # This will fail if the user enters an invalid authorization code
        access_token, user_id = flow.finish(code)
        accessTokenFileOverwrite.write(access_token)
    except:
        print("failed authorization, restart")
        accessTokenFileOverwrite.close()
        os.remove("accessToken.txt")

    accessTokenFileOverwrite.close()


def dropboxUpload(fileToUpload):
    if not os.path.isfile("accessToken.txt"):
        dropboxAuth()

    # get access token from file
    accessTokenFileRead = open("accessToken.txt", "r")
    access_token = accessTokenFileRead.read().rstrip()
    accessTokenFileRead.close()

    # make client
    client = dropbox.client.DropboxClient(access_token)

    # upload file
    fileToUploadObject = open(fileToUpload, "rb")
    response = client.put_file(fileToUpload, fileToUploadObject)
    fileToUploadObject.close()


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
        camera.close()
        print("uploading to Dropbox")
        dropboxUpload(filename)
        print("uploaded to Dropbox")
finally:
    camera.close()
    pir.close()
    GPIO.cleanup() # this ensures a clean exit