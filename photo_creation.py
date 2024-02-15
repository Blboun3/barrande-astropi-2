from picamera import PiCamera
from time import sleep

def photographer(photo_number):
    """_summary_

    Args:
        photo_number (_type_): _description_
    """
    print("photo_creation.py is starting")

    camera = PiCamera()

    # photo taking code beginning

    camera.start_preview()

    # Wait for 4 seconds
    # For camera to properly focus/adjust to light etc.
    sleep(4)

    camera.capture('image%s.jpg' % photo_number)

    camera.stop_preview()

    # photo taking code end

    print("stopping photocreation.py")