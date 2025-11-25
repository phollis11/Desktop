#Calculating mean distance for post office problem

def mean_dist(list):
    #When the list has 1 element, return that element
    if len(list) == 1:
        return list[0]
    #Recursively calculate each smaller mean, 1 element less at a time
    small_mean = mean_dist(list[:-1])    
    n = len(list)
    #When the list has 1 element, return calculation of mean for current length of list
    return ((n-1) * small_mean + list[-1]) / n
    

#Tracing from ChatGPT
def recursive_mean(villages, depth=0):
    indent = "  " * depth  # visual indent for recursion depth
    print(f"{indent}Called with villages = {villages}")

    # Base case
    if len(villages) == 1:
        print(f"{indent}Base case reached. Returning {villages[0]}")
        return villages[0]

    # Recursive call on smaller sublist
    smaller_mean = recursive_mean(villages[:-1], depth + 1)

    # Compute current mean
    n = len(villages)
    current_mean = ((n - 1) * smaller_mean + villages[-1]) / n

    # Show the math
    print(f"{indent}Combining step for n={n}:")
    print(f"{indent}  Smaller mean = {smaller_mean}")
    print(f"{indent}  Last village = {villages[-1]}")
    print(f"{indent}  New mean = (({n - 1}) * {smaller_mean} + {villages[-1]}) / {n} = {current_mean}")

    return current_mean


# Example usage
villages = [0, 10, 20, 14, 223,23, 12]
print("\n--- Tracing recursive_mean ---")
result = recursive_mean(villages)
print("\nFinal mean (optimal post office location):", result)

list = [0, 10, 20]
print(mean_dist(list))

print("\n--- Tracing recursive_mean ---")
result = recursive_mean(list)
print("\nFinal mean (optimal post office location):", result)

    

