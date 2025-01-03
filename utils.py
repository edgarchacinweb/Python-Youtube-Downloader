def seconds_to_hours(seconds):
  hours = seconds // 3600
  minutes = (seconds % 3600) // 60
  seconds = seconds % 60
  return hours, minutes, seconds

def time_to_str(time):
  return (f"{time[0]}".rjust(2, "0") + "h:" + f"{time[1]}".rjust(2, "0") + "m:" + f"{time[2]}".rjust(2, "0") + "s")