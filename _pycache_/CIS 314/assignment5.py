"""
Using this file, you should demonstrate the following:

    Opening the file
    Reading the file into a list
    Filter out / remove log entries from "BotPoke"
    Count the remaining log entries
    Using a regular expression, provide a list of the remaining IP Addresses.*

*If an IP address is repeated, only include it in the list once - unique IPs.
"""

import re

#1

#List to add data to
data = []

#Open file with read
in_file = open(r"C:\Users\pholl\Downloads\access.log", "rt")

#2
print("#2")
#Read each line in file
in_data = in_file.readlines()

#Add each line to data list
for x in in_data:
    data.append(x)

in_file.close()

#Print each line of data seperatly for ease of viewing

for x in data:
    print(x)

#3
print("#3")
#Use shallow copy to remove all botpoke logs
for x in data[:]:
    if "BotPoke" in x:
        data.remove(x)
"""
for x in data:
    print(x)
"""
#4
print("#4")
#Count of remaining data is length of data list
count = len(data)

print("Count of remaining logs is: ", count)

#5
print("#5")
#Used Chat GPT to create regex for finding any valid IP address
# regex for valid IPv4 addresses (0–255 range)
ip_pattern = re.compile(
    r"\b(25[0-5]|2[0-4]\d|1?\d{1,2})(\.(25[0-5]|2[0-4]\d|1?\d{1,2})){3}\b"
)

#Using property of sets to only end up returning list with one of each ip
seen_ips = set()
unique_logs = []

for line in data: #For each line in the data
    match = ip_pattern.search(line) #If the regular expression fits the line then...
    if match: #If match is true 
        ip = match.group(0) #ip becomes entire grouping that the regex found (ie entire IP address)
        if ip not in seen_ips:  #Add ip to set if not in set
            seen_ips.add(ip) #Add ip to set so that same ips later wont get added to final data set
            unique_logs.append(line) #Add the unique log to the final data set

#Print unique logs
for x in unique_logs:
    print(x)



