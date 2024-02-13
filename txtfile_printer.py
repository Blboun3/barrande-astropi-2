

def printer(average_speed):
    """
    printer
    average_speed (float): calculated from 'main.py'
    creates file 'report.txt' containing outcome of our measuring
    """
    report = open('report.txt', 'w')

    report.write("Average speed during our measuring was " + str(average_speed) + "kms^-1")

