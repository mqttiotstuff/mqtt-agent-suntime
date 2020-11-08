import datetime
from suntime import Sun, SunTimeException

# Lyon
latitude = 45.75
longitude = 4.85

sun = Sun(latitude, longitude)

# Get today's sunrise and sunset in UTC
today_sr = sun.get_sunrise_time()
today_ss = sun.get_sunset_time()
print('Today at Lyon the sun raised at {} and get down at {} UTC'.
      format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))

# On a special date in your machine's local time zone
abd = datetime.date(2020, 9, 25)
abd_sr = sun.get_local_sunrise_time(abd)
abd_ss = sun.get_local_sunset_time(abd)
print('On {} the sun at Lyon raised at {} and get down at {}. local time'.
      format(abd, abd_sr.strftime('%H:%M'), abd_ss.strftime('%H:%M')))

