from picamera import PiCamera
from time import sleep

print("photo_creation.py is starting")

camera = PiCamera()

# photo taking code beginning

camera.start_preview()

# loop for capturing 42 photos at 10 sec intervals

for i in range(42):
    sleep(10)
    camera.capture('image%s.jpg' % i)

camera.stop_preview()

# photo taking code end

print("stopping photocreation.py")