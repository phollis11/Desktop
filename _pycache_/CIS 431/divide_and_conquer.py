#Divide and Conquer Assignment

#Mergesort algorithm
def mergesort(list):
    #Base case, if list len is 1, return list
    if len(list) == 1:
        return list
    #Divide the list into left and right halves
    mid = len(list) //2
    left = list[:mid]
    right = list[mid:]
    #Make recursive calls on left and right halves until list len is 1
    left_half = mergesort(left)
    right_half = mergesort(right)
    #Return function call that sorts the left and right halves while combining into 1 list
    return merges(left_half, right_half)

#Merges funtion
def merges(left_half, right_half):
    #Empty solution list
    sorted_list = []
    #Pointers for left and right lists
    i = 0 
    j = 0
    #Use pointers to look through each left and right half
    while i < len(left_half) and j < len(right_half):
        #If value in left half at pointer i is less than value of right half at pointer j
        if left_half[i] < right_half[j]:
            #Append to solution list left_half[i]
            sorted_list.append(left_half[i])
            #Increment i pointer to next value
            i += 1
        else: #Otherwise, vice versa must be true
             sorted_list.append(right_half[j])
             j += 1
    #If there are any remaining values in left side of array add to solution list
    while i < len(left_half):
        sorted_list.append(left_half[i])
        i += 1
    #If there are any remaining values in right side of array add to solution list
    while j < len(right_half):
        sorted_list.append(right_half[j])
        j += 1
    #Return the sorted list
    return sorted_list

#Hoare Partition Algorithm
def hoare_partition(arr, low, high):
    #Create pivot and pointers
    pivot = arr[low]
    i = low - 1
    j = high + 1
    while True:
        # Move i to the right until arr[i] >= pivot
        i += 1
        while arr[i] < pivot:
            i += 1
        # Move j to the left until arr[j] <= pivot
        j -= 1
        while arr[j] > pivot:
            j -= 1
        # If pointers meet or cross, return partition index
        if i >= j:
            return j
        # Swap elements
        arr[i], arr[j] = arr[j], arr[i]

#Quicksort Algorithm
def quicksort(arr, low, high):
    #Low and high are first and last elements of array
    if low < high:
        #If low is smaller than high, partition the array
        p = hoare_partition(arr, low, high)
        #Recursvively call the algorithm on the left and right sides
        quicksort(arr, low, p)
        quicksort(arr, p + 1, high)
    
if __name__ == "__main__":
    #Mergesort Tests
    print("Mergesorts: ")
    list  = [3, 4, 1, 5, 6, 2]
    sorted_list = mergesort(list)
    print(sorted_list)

    list2 = [1,6,2,8,0,43,63,32,1,56,73,235]
    sorted_list2 = mergesort(list2)
    print(sorted_list2)

    print("Quicksorts: ")
    #Quicksort tests
    arr1 = [8, 3, 1, 7, 0, 10, 2]
    quicksort(arr1, 0, len(arr1) - 1)
    print(arr1)

    arr2 = [12,64,23,52,1,53,6,4,32]
    quicksort(arr2, 0, len(arr2) - 1)
    print(arr2)