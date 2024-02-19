if __name__ == "__main__":
    from measure_speed import measure_speed
    from photo_creation import photographer
    import time
    from txtfile_printer import printer
    import statistics
    from logzero import logger, logfile
    from picamera import PiCamera

    # set log file
    logfile("events.log")

    # variables for time keeping
    time_start = time.time()
    time_end = (time.time() + 540)

    # true while we have time (i.e. runtime is less than 540 seconds (= 9 minutes))
    haveWeTime = True

    # file name numbering
    photo_number = 0
    picforcomp_1 = None
    picforcomp_2 = None

    #average velocity calculation
    average_velocity = None
    velocity_median = None
    deviation_max = None # median + 10%
    deviation_min = None # median - 10%

    # Array containing all measured velocities
    velocity = []

    # variable debugging
    logger.info(f'Start time: {time_start}')
    logger.info(f'Expected end time: {time_end}')

    # start camera
    camera = PiCamera()
    camera.resolution = (4056,3040)

    i = 0

    # main loop
    while haveWeTime == True:
        loop_start = time.time()
        logger.info(f'OK, we have time. Loop nr. {i} started at {loop_start}')


        # !!! 1st photo name image0.jpg
        if photo_number == 0:
            logger.info("Photo_creation.py is starting")
            photographer(photo_number, camera)
            logger.info("Stopping photo_creation.py")
        else:
            pass

        photo_number = photo_number + 1
        logger.info("Photo_creation.py is starting")
        photographer(photo_number, camera)
        logger.info("Stopping photo_creation.py")

        # comparison between latest and previous photo
        picforcomp_1 = photo_number - 1 # previous photo
        picforcomp_2 = photo_number # current photo
        currentSpeed = measure_speed(f'image{picforcomp_1}.jpg', f'image{picforcomp_2}.jpg')
        logger.info(f'Measured speed: {currentSpeed}')
        velocity.append(currentSpeed)

        # 9 minutes runtime = 540 seconds
        # limited to 42 photos
        # 540 seconds divided by 42 photos
        """
        # ~Average time per one cycle of this loop should be around 12 seconds~
        # ~current time - loop start time = how long has the loop ran for~
        # ~12 - that = how long until 12 seconds~
        """
        # Replaced by static 16 seconds, it took to long to take the photos

        sleepTime = 15 - (time.time() - loop_start)
        if(sleepTime < 0):
            sleepTime = 0
        logger.info(f'Sleeping for {sleepTime}; Loop ran for {time.time() - loop_start}')
        i += 1
        time.sleep(sleepTime)

        #check if we have time
        if time.time() < time_end:
            haveWeTime = True
        else:
            logger.info("Time run out, exiting main loop")
            haveWeTime = False
            break

    #calculating average speed
    logger.info(f'Measured speeds array {velocity}')
    velocity_median = str(statistics.median(velocity))[:6]
    logger.info(f'Calculated average speed {velocity_median}')

    deviation_max = velocity_median * 1.1
    deviation_min = velocity_median * 0.9

    # creates file 'report.txt' containing final resault
    printer(average_velocity)

    camera.close()
    # End
    logger.info("Program ended /nReport containing outcome of our measuring can be found in report.txt")