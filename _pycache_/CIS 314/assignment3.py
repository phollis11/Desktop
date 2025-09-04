import random

#1
#Tuple and Dictionary

print("#1")

penguins = ("Crosby", "Malkin", "Letang", "Karlsson", "Rust"
        , "Rakell" ,"Jarry", "Acciari", "Imama", "McGroarty")

positions = {
        "McGroarty" : "RW", 
        "Imama" : "LW", 
        "Acciari" : "C",
        "Jarry" : "G", 
        "Rakell" : "RW",
        "Rust" : "RW",
        "Karlsson" : "D",
        "Letang" : "D",
        "Malkin" : "C",
        "Crosby" : "C"
}

#2
#Prints 3rd element in tuple and dictionary
print("#2")
print(penguins[2] + " and "  + list(positions.items())[2][0] +" "+ list(positions.items())[2][1])

#3
#Fills a temporary list with the tuple to allow order to be randomized using import random
print("#3")
temp_list = []
for x in penguins:
    temp_list.append(x)

random.shuffle(temp_list)
print(temp_list)

#Uses list() to convert dictionary to list and then shuffles and prints

dictionary_list  = list(positions.items())
random.shuffle(dictionary_list)
print(dictionary_list)

#4
#Uses temp list to allow appending and then converts back to tuple
print("#4")
temp_list2 = []
for x in penguins:
    temp_list2.append(x)

temp_list2.append("Heinen")

penguins = tuple(temp_list2)
print(penguins)

#Uses update to add element

positions.update({"Hienen" : "LW"} )
print(positions)

#5
#Uses temp list to allow removal and then converts back to tuple
print("#5")

temp_list3 = []
for x in penguins:
    temp_list3.append(x)

temp_list3.pop(0)

penguins = tuple(temp_list3)  
print(penguins)

#Uses iter and del to remove first item in dict

del positions[next(iter(positions))]
print(positions)

#6
#Remove same item by first removing from tuple and then searching dictionary for that key
#This removes Karlsson from both tuple and dictionary 

print("#6")

temp_list4 = []
for x in penguins:
    temp_list4.append(x)
key = temp_list4[2]
temp_list4.pop(2)

print(temp_list4)

del positions[key]
print(positions)