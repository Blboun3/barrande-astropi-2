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


def median(data):
    """Return the median (middle value) of numeric data.

    When the number of data points is odd, return the middle data point.
    When the number of data points is even, the median is interpolated by
    taking the average of the two middle values

    Standard function from statistics library
    """
    try:
        data = [i for i in data if i is not None]
        data = sorted(data)
        n = len(data)
        if n == 0:
            return None
        if n % 2 == 1:
            return data[n // 2]
        else:
            i = n // 2
            return (data[i - 1] + data[i]) / 2
    except Exception:
        return None
