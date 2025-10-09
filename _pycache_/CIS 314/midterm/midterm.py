import csv, tkinter as tk, os, webbrowser, player_lookup
#player_lookup is my own module. This module contains functions for creating the player_dictionary

#ALL DATA COMES FROM MoneyPuck.com

#Sets up main frame, root, of tkinter ui
root = tk.Tk() 
root.title("Lookup Stats for NHL Players")
root.geometry("700x500")

#Function for creating a dictionary with playerName : playerId key-value pairs
#Allows a user to either lookup players by nhl id or there full name
player_dict = player_lookup.build_dictionary()
    
#Main function that runs when user requests data by clicking the submit button
#All important processes run when submit is clicked
def on_submit():

    player_id = entry.get() #Retrieve value in entry bar
    season_selected = dropdown_var.get() #Retrieve value in dropdown menu
    game_count = 0 #Variable for counting games
    result_text.config(state="normal") #Sets result text to be edited by program
    season_text.config(state="normal") #Sets season text to be edited by program
    result_text.delete(1.0, tk.END) #Wipes any data already in text box
    season_text.delete(1.0, tk.END) #Wipes any data already in text box

    #Try except statement for seeing if entry value is a nhl id or a name
    try:
        if not player_id.isdigit(): #If the entry is not a digit, aka player id
            player_id = player_lookup.id_lookup(player_id) #Switches entry value of name to player id using player dictionary
                                                            #This is used to find file path
    except KeyError: 
        #Catches key error and notifies user of an issue
        season_text.delete(1.0, tk.END)
        season_text.insert(tk.END, "Player id or name not recognized. Please try again." \
                                    "Click the button below to retrieve data for the desired player.")
        

    #File path used to find needed data on computer, must be switched if using a different computer or file location
    base_path = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\CIS 314\midterm" #Base file path for finding csv file
    file_num = str(player_id)  #Ensure file_num is a string
    file_path = os.path.join(base_path, f"{file_num}.csv") #os function that joins the base path with the file number

    total_goals, total_assists, total_points = 0, 0, 0  # initialize counters

    #Try except statement for opening csv file of player data
    try:
        with open(file_path, newline="") as csv_in:
            reader = csv.DictReader(csv_in)
            for row in reader: #For each row, Add stats for season selected for each complete game by player

                if  row["season"] == season_selected and row["situation"] == "all":
                    game_count += 1 #Increment total game count
                    #Insert into result text a few specific values
                    result_text.insert(tk.END,
                        f"Player Team: {row['playerTeam']}, "
                        f"Opposing Team: {row['opposingTeam']}, "
                        f"Icetime: {row['icetime']}, "
                        f"Shifts: {row['shifts']}, "
                        f"On Ice xGoals For: {row['OnIce_F_xGoals']}, "
                        f"Primary Assists: {row['I_F_primaryAssists']}, "
                        f"Secondary Assists: {row['I_F_secondaryAssists']}, "
                        f"On Ice xGoals Against: {row['OnIce_A_xGoals']}\n\n"
                    )
                    #If statements for handling if value is 0, tells function to skip if the value is 0
                    #Solved issues since data writes 0 as a string and not number for some reason
                    if row["I_F_goals"] != "0.0":
                        total_goals += float(row["I_F_goals"]) #Increments total goals
                    if row["I_F_points"] != "0.0":
                        total_points += float(row["I_F_points"]) #Increments total points

    #If the file is not found, tell the user to recheck spelling, or downlaod the data
    except FileNotFoundError:
        season_text.delete(1.0, tk.END)
        season_text.insert(tk.END, "No file found for entered player. Re-check id or name. " \
                                    "Click the button below to retrieve data for the desired player.")

    total_assists = total_points - total_goals  #Calculates total assists by using points and goals

    #If the player didnt play in a season, then say there is no data
    if game_count > 0:
        #Else give averages for the season
        season_text.insert(tk.END,
            f"Total Goals: {total_goals}, Per Game: {round(total_goals/game_count, 3)}\n "
            f"Total Assists: {total_assists}, Per Game: {round(total_assists/game_count, 3)}\n"
            f"Total Points: {total_points}, Per Game: {round(total_points/game_count, 3)}\n"
            f"Games Played: {game_count}"
        )
    else:
        result_text.insert(tk.END, "No data found for this player in the selected season.")
    
    #Set the result and season text to disabled so it cannot be edited by user
    result_text.config(state="disabled")
    season_text.config(state="disabled")

#UI Widgets

#Main frame for ui in root
frame = tk.Frame(root)
frame.pack(fill= "x")

#Creates a text label
label = tk.Label(frame, text="Enter a player's NHL ID number or their full name below:")
label.grid(row = 0, column = 0) #Using grid packing to have control over location of label

#Entry box for entering player_id or name
entry = tk.Entry(frame, width=25)
entry.grid(row = 1, column = 0, padx = 20, pady = 2.5) #Grid packing

#Submit button, calls function on_submit() when clicked
submit = tk.Button(frame, text="Submit", command=on_submit)
submit.grid(row = 2, column = 0, padx = 20, pady=2.5) #Grid packing

#List of years to choose from, 2000-2025 since only for modern players
years = ["2000", "2001", "2002", "2003", "2004", "2005", "2006", 
         "2007", "2008", "2009", "2010", "2011", "2012", "2013", 
         "2014", "2015", "2016", "2017", "2018", "2019", "2020",
         "2021", "2022", "2023", "2024", "2025"]

#Create dropdown box, set intitial value to 2000
dropdown_var = tk.StringVar(frame)
dropdown_var.set(years[0])

#When the dropdown is clicked, open the dropdown variable containing all the years
dropdown_menu = tk.OptionMenu(frame, dropdown_var, *years)
dropdown_menu.grid(row = 3, column = 0, padx = 20, pady=2.5) #Grid packing

#Label for creating seasons stats
label2 = tk.Label(frame, text ="Seasons Stats: ")
label2.grid(row = 0, column = 1, padx = 20) #Grid packings

#Season values textbox
season_text = tk.Text(frame ,wrap = "word", width = 40, height = 5)
season_text.grid(row = 1, column = 1, padx = 20, pady = 5) #Grid packing

#Webbrowser link 
def open_link():
    webbrowser.open("https://moneypuck.com/data.htm") #Opens up webbrowser used to retrieve player data

#Button for retrieving data
link_button = tk.Button(frame, text = "Retrieve Data", command = open_link)
link_button.grid(row = 2, column = 1) #Grid packing

#Creating a second frame for lower textbox
frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=5, pady=5) #Standard pack

#Creating scrollbar in 2nd frame
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

#Label for game stats
label3 = tk.Label(frame, text = "Game Stats: ")
label3.pack() #Standard pack

#Result textbox, with scrollbar
result_text = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set)
result_text.pack(fill="both", expand=True) #Standard pack
scrollbar.config(command=result_text.yview)

# Make text read-only
result_text.config(state="disabled")
season_text.config(state="disabled")

#When ran mainloop keeps UI running
if __name__ == "__main__":
    root.mainloop()




 