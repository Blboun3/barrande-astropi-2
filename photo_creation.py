from time import sleep

def photographer(photo_number, camera):
    """Function to take and save photo

    Args:
        photo_number (number): sequential ID of the photo, used for naming the saved file
    """
    print("photo_creation.py is starting")

    # photo taking code beginning

    camera.start_preview()
    # Wait for 4 seconds
    # For camera to properly focus/adjust to light etc.
    #sleep(4)
    camera.capture('image%s.jpg' % photo_number)

    camera.stop_preview()
    # photo taking code end
    print("stopping photo_creation.py")