#Use a built in python 
#module to create a basic Python file
#Basic datetime import
#Finds difference between now and a later date

from datetime import datetime

now = datetime.now()

later = datetime(2025, 9, 7, 1, 0 , 0)

time_till = later - now

print(now)
print(later)
print(f"Time difference: {time_till}" )