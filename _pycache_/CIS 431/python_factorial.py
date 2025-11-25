"""
Compose four distinct programs that compute the factorial of a specified integer value, once for a modest integer and once for a considerably larger integer. Each program should be developed twice: once utilizing a while loop and once employing a method in both Java and Python.

Upon executing the programs, you are required to articulate your reflections regarding your observations in terms of efficiency of each program.

write your report in doc format with the screen shot of your output and upload your code 
"""
import timeit

def factorial_loop(int):
    sum = int
    while int > 1:
        sum = sum *(int - 1)
        int -= 1
    return sum

def factorial_recurse(int):
    if int == 0:
        return 1
    else:
        return int * factorial_recurse(int - 1)
    
#Execution times for using looping method
execution_time_15 = timeit.timeit(lambda: factorial_loop(15), number = 10000)
execution_time_50 = timeit.timeit(lambda: factorial_loop(50), number = 10000)
execution_time_100 = timeit.timeit(lambda: factorial_loop(100), number = 10000)

#Execution times for using recursive method
r_execution_time_15 = timeit.timeit(lambda: factorial_recurse(15), number = 10000)
r_execution_time_50 = timeit.timeit(lambda: factorial_recurse(50), number = 10000)
r_execution_time_100 = timeit.timeit(lambda: factorial_recurse(100), number = 10000)



print("Loop Execution time for 15: " + str(execution_time_15))
print("Loop Execution time for 50: " + str(execution_time_50))
print("Loop Execution time for 100: " + str(execution_time_100))

print("Recursive Execution time for 15: " + str(r_execution_time_15))
print("Recursive Execution time for 50: " + str(r_execution_time_50))
print("Recursive Execution time for 100: " + str(r_execution_time_100))

print("Factorial 15: " + str(factorial_recurse(15)))
print("Factorial 50: " + str(factorial_recurse(50)))
print("Factorial 100: " + str(factorial_recurse(100)))




