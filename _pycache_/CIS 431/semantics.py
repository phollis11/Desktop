#Python Program random number guesser

import random

def game():
    print("Welcome to the game")
    print("I am thinking of a number 1-100")

    random_num = random.randint(1,100)
    attempts = 0
    guess = None

    while guess != random_num:
        try:
            guess = int(input("Guess a number 1-100"))
            attempts +=1
            if guess < random_num:
                print("Too small, try again")
            elif guess > random_num:
                print("Too large, try again")
            else:
                print(f"Congrats, it took {attempts} attempts")
        except ValueError:
            print("Please enter a valid number")
        

game()
