from datetime import datetime

dt = datetime.now()
hr = str(dt.hour)
print(dt)
print(dt.date())
print(dt.date().weekday())
print(dt.year)
print(dt.month)
print(hr)
print(dt.minute)
print(dt.second)