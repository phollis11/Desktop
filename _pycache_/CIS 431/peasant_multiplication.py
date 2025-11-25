#Peasant Multiplication implementation, Function takes two integers
def peasant_multi(num1, num2): 
    #Edge cases if either number is negative or 0
    if num1 == 0 or num2 == 0:
        return 0 #Return 0 if either is negative
    #If num1 is negative and num2 is positive
    if num1 < 0 and num2 > 0:
        #Call function again but with absolute value of num1, then switch sign at end to make negative
        return peasant_multi(abs(num1), num2) * -1
    if num1 > 0 and num2 < 0:
        #Call function again but with absolute value of num2, then switch sign at end to make negative
        return peasant_multi(num1, abs(num2)) * -1
    if num1 < 0 and num2 < 0 :
        #Call function again but with absolute value of num1 and num2, sign doesnt need to change then
        return peasant_multi(abs(num1), abs(num2))
    #List is used to store values of num2 if num1 is odd
    list  =  []
    #Catch first number, if num1 is odd, append num2 to list
    if num1 %2 != 0:
        list.append(num2)
    #While num1 is not 1 keep loop running
    while num1 != 1:
        #Divide num1 by 2 using integer division, gets rid of remainder since it is not needed
        num1 = num1 // 2 
        #Multiply num2 by 2
        num2 = num2 * 2 
        #If num1 is odd, append num2 to list
        if num1 %2 != 0:
            list.append(num2)
    #Sum all values in list and return result
    return sum(list)


#Function for generating permutations of lists
def gen_permutes(elements):
    #Base case if list is empty, used to stop recursive loops
    if len(elements) == 0:
        return [[]]
    #List for permutations to be appended to
    permutations = []
    #For each number in the length of original list
    for i in range(len(elements)):
        #Store the current element for the start of the permutation
        current = elements[i]
        #Store the remaining elements to make recursive call
        remaining = elements[:i] + elements[i+1:]
        #For each number in the list, recursive call the remaining elements to go through all permutations
        for p in gen_permutes(remaining):
            #Append to the current list and current permutation, 
            permutations.append([current] + p)
    #Return full list
    return permutations

#Testing
if __name__ == "__main__":
    print("Peasant Mult Testing: ")
    print("0 x 2473489 = ", peasant_multi(0, 2473489)) #0
    print("-2 x 2 = ", peasant_multi(-2, 2)) #-4
    print("2 x -5 = ", peasant_multi(2, -5))#-10
    print("-5 x -9 = ", peasant_multi(-5, -9)) #45
    print("10 x 43 = ",peasant_multi(10, 43)) #430
    print("3 x 13 = ",peasant_multi(3, 13)) #39
    print("23 x 436 = ", peasant_multi(23, 436)) #10028

    print("Permutes Testing: ")
    print("[]: " , gen_permutes([]))
    print("[1, 2, 3]: ", gen_permutes([1, 2, 3]))
    print("[Cat, Dog, Fish, Hamster]: ", gen_permutes(["Cat", "Dog", "Fish", "Hamster"]))