import random
import secrets
import timeit
from collections import Counter

""""
    Comparing small numbers
        Fill a data structure with 100 random numbers between 1 and 16 using Python `random`
        Fill a data structure with 100 random numbers between 1 and 16 using a different Python RNG/PRNG module (`os`, `secrets`, or something from PyPi)
        Get a count of the unique numbers in each data structure
        ie: how many times does the number 1 appear? What about 2? 3?
        Based on the counts, does one method appear better than the other?
    Run #1 again using numbers 1-65535, is 1.4. any different? Are any numbers repeated for either data set?

    Create a 100-element list with random numbers between 1-16
        Write a function to sort the list using your own code (for/while loops OR your implementation of one of the sorting algorithms we discussed) and print the amount of time it takes to run
        Time how long it takes using .sort()
    Do #3 again but with a 100-element list with numbers between 1-65535, does the sorting time change? Is one more efficient with larger numbers?
    Do #4 again, but with 500-element list, does the sorting time change? Does one method flounder on larger data sets?
"""


#1
print("#1")
#Fill list using random
random_list = []
i = 0
while i < 100:
    random_list.append(random.randint(1,16))
    i += 1

print("List using random: ")
print(random_list)

#Fill list using secrets
secrets_list = []
i = 0 
while i < 100:
    secrets_list.append((secrets.randbelow(16) +1))
    i += 1

print("List using secrets: ")
print(secrets_list)

#Get count of how many times each value repeats using random
random_list_count = {}
i = 1
while i < 17:
    count = random_list.count(i) #Use count to find how many times each value is seen
    random_list_count.update({i : count}) #Update dictionary with value and how many times it was seen
    i += 1

print("Count of random list: ")
print(random_list_count)

#Get count of how many times each value repeats using secrets
secrets_list_count = {}
i = 1
while i < 17:
    count = secrets_list.count(i)
    secrets_list_count.update({i : count})
    i += 1

print("Count of secrets list: ")
print(secrets_list_count)

#Values appear to be equally random. However, random should only be used when there is no need for security. Secrets
#is cryptographically secure. 

#2
print("#2")

#Repeat #1 except using ints from 1 to 65535
random_list2 = []
i = 0
while i < 100:
    random_list2.append(random.randint(1,65535))
    i += 1

print("Random list with new ints: ")
print(random_list2)

secrets_list2 = []
i = 0 
while i < 100:
    secrets_list2.append((secrets.randbelow(66535) +1))
    i += 1

print("Secrets list with new ints: ")
print(secrets_list2)

#Changed previously used method of counting since it is very inefficient for this large span of numbers
#Found python module that does this efficiently

#Counter takes a list and returns a dictionary with how many times each value is repeated. Efficient since it only iterates once.
random_list_count2 = Counter(random_list2)

print("Count of random list: ")
print(random_list_count2)

secrets_list_count2 = Counter(secrets_list2)

print("Count of secrets list: ")
print(secrets_list_count2)

#3
print("#3")

#Create random list with 100 elements
ran_list = []
i = 0
while i < 100:
    ran_list.append(random.randint(1,16))
    i += 1

#Copy list now so that it can be sorted using own method and .sort() method
copy_list = ran_list

#Implementation of simple bubble sort algorithm
def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

#Timeit.timeit takes method and times how long it takes to run
#Found out that lambda must be used to allow the function to take the parameters it needs
#Decided to run 10000 times so that execution time is easier to compare
execution_time = timeit.timeit(lambda: bubble_sort(ran_list), number=10000)
copy_list_execution_time = timeit.timeit(lambda: copy_list.sort(), number=10000)

#Sort lists using both methods
bubble_sort(ran_list)
copy_list.sort()

print("Sorted list: ")
print(ran_list)
print("Execution time: ")
print(execution_time)

print("Sorted copy list: ")
print(copy_list)
print("Execution time: ")
print(copy_list_execution_time)

#4

#Create another random list but using larger span of ints
ran_list2 = []
i = 0
while i < 100:
    ran_list2.append(random.randint(1,66535))
    i += 1

#Copy list now so that it can be sorted using own method and .sort() method
copy_list2 = ran_list2

#Use timeit.timeit again for timing exection time
execution_time2 = timeit.timeit(lambda: bubble_sort(ran_list2), number=10000)
copy_list_execution_time2 = timeit.timeit(lambda: copy_list2.sort(), number=10000)

#Sort lists
bubble_sort(ran_list2)
copy_list2.sort()

print("Sorted list: ")
print(ran_list2)
print("Execution time: ")
print(execution_time2)

print("Sorted list: ")
print(copy_list2)
print("Execution time: ")
print(copy_list_execution_time2)

#5
print("#5")

#Create random list with 500 elements
ran_list3 = []
i = 0
while i < 500:
    ran_list3.append(random.randint(1,66535))
    i += 1

#Copy list for using different sorts
copy_list3 = ran_list3

#Timeit.timeit
execution_time3 = timeit.timeit(lambda: bubble_sort(ran_list3), number=10000)
copy_list_execution_time3 = timeit.timeit(lambda: copy_list3.sort(), number=10000)

#Sort lists
bubble_sort(ran_list3)
copy_list3.sort()

print("Sorted list: ")
print(ran_list3)
print("Execution time: ")
print(execution_time3)

print("Sorted list: ")
print(copy_list3)
print("Execution time: ")
print(copy_list_execution_time3)

#Comparisons

print("100 Elements:" \
" Bubble sort: "+ str(execution_time) + "   .sort(): " + str(copy_list_execution_time))
#Bubble sort seems to take slightly longer to execute

print("100 Elements, larger numbers:" \
" Bubble sort: "+ str(execution_time2) + "   .sort(): " + str(copy_list_execution_time2))
#Shows little to know difference in sort times for 100 elements even with larger numbers when compared to previous execution time

print("500 Elements:" \
" Bubble sort: "+ str(execution_time3) + "   .sort(): " + str(copy_list_execution_time3))
#Bubble sort takes significantly longer than .sort() for 500 element list

#Bubble sort is worse for larger data sets than .sort()
