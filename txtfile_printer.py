

def printer(average_speed):
    """Function to save the final speed into report.txt file

    Args:
        average_speed (float): calculated from 'main.py'
    """
    try:    
        with open("report.txt", "w", buffering=1) as f:
            f.write("Average speed during our measuring was " + str(average_speed) + "kms^-1")
            f.close()
    except Exception as e:
        print(f'Unable to write to file due to ${e} error')

