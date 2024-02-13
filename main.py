from photo_creation import photographer
import time
from txtfile_printer import printer

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
numberofvelocities = None
cycles = 0
velocitysum = 0

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

# how many numbers does array have
numberofvelocities = len(velocity)

# adding all velocities together
while cycles <= numberofvelocities:

    velocitysum = velocitysum + velocity[cycles]
    cycles = cycles + 1

# deviding velocitysum by numberof velocities will result in final average velocity
average_velocity = velocitysum / numberofvelocities


# creates file 'report.txt' containing final resault
printer(average_velocity)

# konec
print("program ended /n report containing outcome of our measuring can be found in report.txt")


