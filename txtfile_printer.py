def printer(average_speed):
    """Function to save the final speed into report.txt file

    Args:
        average_speed (float): calculated from 'main.py'
    """
    try:    
        with open("report.txt", "w", buffering=1) as f:
            f.write(str(average_speed))
            f.close()
    except Exception as e:
        print(f'Unable to write to file due to ${e} error')

