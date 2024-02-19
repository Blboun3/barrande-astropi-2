if __name__ == "__main__":
    from measure_speed import measure_speed
    from photo_creation import photographer
    import time
    from txtfile_printer import printer
    import statistics
    from picamera import PiCamera

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
    print(time_start)
    print(time_end)

    # start camera
    camera = PiCamera()
    camera.resolution = (4056,3040)

    # main loop
    while haveWeTime == True:
        print("OK, we have time")

        loop_start = time.time()

        # !!! 1st photo name image0.jpg
        if photo_number == 0:
            photographer(photo_number, camera)
        else:
            pass

        photo_number = photo_number + 1
        photographer(photo_number, camera)

        # comparison between latest and previous photo
        picforcomp_1 = photo_number - 1 # previous photo
        picforcomp_2 = photo_number # current photo
        velocity.append(measure_speed(f'image{picforcomp_1}.jpg', f'image{picforcomp_2}.jpg'))

        # 9 minutes runtime = 540 seconds
        # limited to 42 photos
        # 540 seconds divided by 42 photos  
        # Average time per one cycle of this loop should be around 12 seconds
        # current time - loop start time = how long has the loop ran for
        # 12 - that = how long until 12 seconds

        sleepTime = 12 - (time.time() - loop_start)
        if(sleepTime < 0):
            sleepTime = 0

        time.sleep(sleepTime)

        #check if we have time
        if time_start < time_end:
            haveWeTime = True
        else:
            haveWeTime = False
            break

    #calculating average speed
    velocity_median = statistics.median(velocity)
    print(velocity_median)

    deviation_max = velocity_median * 1.1
    deviation_min = velocity_median * 0.9

    # creates file 'report.txt' containing final resault
    printer(average_velocity)

    # End
    print("program ended /nReport containing outcome of our measuring can be found in report.txt")