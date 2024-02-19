

def printer(average_speed):
    """Function to save the final speed into report.txt file

    Args:
        average_speed (float): calculated from 'main.py'
    """
    try:    
        report = open('report.txt', 'w')
        report.write("Average speed during our measuring was " + str(average_speed) + "kms^-1")
        report.close()
    except Exception as e:
        print(f'Unable to write to file due to ${e} error')


