from photo_creation import photographer
import time
from txtfile_printer import printer
import statistics

#       start of the program

#   variable declaration

# variables for time keeping
time_start = time.time()
time_end = (time.time() + 570)
mamecas = True

# file name numbering
photo_number = 0
picforcomp_1 = None
picforcomp_2 = None

#average velocity calculation
average_velocity = None
velocity = []
velocity_median = None
deviation_max = None # median + 10%
deviation_min = None # median - 10%

# variable debugging
print(time_start)
print(time_end)

while mamecas == True:
    print("mamecas")

    # !!! 1st photo name image0.jpg

    if photo_number == 0:
        photographer(photo_number)
    else:
        pass

    photo_number = photo_number + 1

    photographer(photo_number)

    # comparison between latest and previous photo
    picforcomp_1 = photo_number -1
    picforcomp_2 = photo_number
    measure_speed(picforcomp_1, picforcomp_2)




    #check for time
    if time_start < time_end:
        mamecas = True
    else:
        mamecas = False
        break


#calculating average speed

velocity_median = statistics.median(velocity)
print(velocity_median)

deviation_max = velocity_median * 1.1
deviation_min = velocity_median * 0.9




# creates file 'report.txt' containing final resault
printer(average_velocity)

# konec
print("program ended /n report containing outcome of our measuring can be found in report.txt")


