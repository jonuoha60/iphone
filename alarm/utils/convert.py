def convert_to_24hr(hour_12, ampm):
    """Convert 12-hour format to 24-hour format"""
    hour = int(hour_12)
    if ampm == "AM":
        return 0 if hour == 12 else hour
    else:  # PM
        return hour if hour == 12 else hour + 12