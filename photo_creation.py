from picamera import PiCamera
from time import sleep

def photographer(photo_number):
    print("photo_creation.py is starting")

    camera = PiCamera()

    # photo taking code beginning

    camera.start_preview()

    # loop for capturing 42 photos at 10 sec intervals

    sleep(4)

    camera.capture('image%s.jpg' % photo_number)

    camera.stop_preview()

    # photo taking code end

    print("stopping photocreation.py")