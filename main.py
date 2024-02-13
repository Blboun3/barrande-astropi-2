from photo_creation import photographer
import time

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


# konec
print("program ukoncen")


