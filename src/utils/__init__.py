from datetime import datetime, timedelta

def calculate_n(input_date):
    current_year = datetime.now().year
    date = datetime.strptime(f"{input_date} {current_year}", "%b %d %Y")
    jan_1 = datetime(year=current_year, month=1, day=1)
    delta = date - jan_1
    return delta.days + 1  # Include Jan 1 as day 1

def calculate_local_standard_meridian(longitude):
    """
    Calculate the Local Standard Meridian (LST) based on the given longitude.

    :param longitude: Longitude in degrees (positive for East, negative for West)
    :return: Local Standard Meridian (LST) in degrees
    """
    # Local Standard Meridian is typically a multiple of 15 degrees
    l_st = round(longitude / 15) * 15
    print(f"Given longitude: {longitude}° => Local Standard Meridian: {l_st}°")
    return l_st

def time_to_hour_angle(time_str):
    """
    Convert time in HH:MM:SS format to hour angle in degrees.

    :param time_str: Time as a string in HH:MM:SS format.
    :return: Hour angle in degrees.
    """
    # Split the time string into hours, minutes, and seconds
    hours, minutes, seconds = map(int, time_str.split(':'))

    # Convert the time into total seconds
    total_seconds = (hours - 12) * 3600 + minutes * 60 + seconds
    
    # Calculate the fraction of the day
    fraction_of_day = total_seconds / 86400  # 86400 seconds in a day (24 * 60 * 60)
    
    # Calculate the hour angle in degrees
    hour_angle = fraction_of_day * 360  # 360 degrees for a full day
    
    print(f"Time: {time_str} -> Hour Angle: {hour_angle}°")
    return hour_angle