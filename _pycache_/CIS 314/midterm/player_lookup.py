#Use this as a one place stop to place all players and there id into a dictionary
#Call this from midterm.py to access dictionary

import csv

player_dict = {}

def build_dictionary():
    with open(r"C:\Users\pholl\OneDrive\Desktop\_pycache_\CIS 314\midterm\allPlayersLookup.csv", newline="") as csv_in:
        reader = csv.DictReader(csv_in)
        for row in reader:
            player_dict.update({row['name'] : row['playerId']})
    return player_dict

#Function that is called if there is a name requested, used to flip name to playerId for file pathing purposes
def id_lookup(name):
    return player_dict[name]
    

if __name__ == "__main__":
    build_dictionary()
    print(player_dict)