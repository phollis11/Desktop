import sys, os, admin, golf_ai
import golf_globals as globals
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QWidget, QVBoxLayout, QMessageBox, QGridLayout, QSizePolicy, QComboBox, QLabel, QTableView, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtPositioning import QGeoPositionInfoSource
from geopy.distance import distance

#Stylesheet
GOLFSHEET = """
/* -----------------------------------------
   GOLF THEME FOR PYQT5
   Fairway Green: #2e7d32
   Rough Green: #a5d6a7
   Sand Trap Tan: #f4e7c6
   Deep Turf: #1b5e20
   Ball White: #ffffff
------------------------------------------ */

QWidget {
    background-color: #a5d6a7;
    color: #1b5e20;
    font-family: Segoe UI, sans-serif;
    font-size: 14px;
}

/* ----- Buttons ----- */
QPushButton {
    background-color: #2e7d32;
    color: white;
    border-radius: 12px;
    padding: 8px 15px;
    border: 2px solid #1b5e20;
}

QPushButton:hover {
    background-color: #1b5e20;
}

QPushButton:pressed {
    background-color: #154a18;
}

/* ----- Labels ----- */
QLabel {
    font-size: 15px;
}

/* ----- Line Edits ----- */
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
    background-color: #ffffff;
    border: 2px solid #2e7d32;
    border-radius: 8px;
    padding: 6px;
    color: #1b5e20;
}

QLineEdit:focus, QTextEdit:focus {
    border-color: #1b5e20;
}

/* ----- ComboBox ----- */
QComboBox {
    background-color: #ffffff;
    border: 2px solid #2e7d32;
    border-radius: 8px;
    padding: 5px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    selection-background-color: #2e7d32;
    border-radius: 0px;
}

/* ----- TableView / ListView ----- */
QTableWidget, QTableView, QListWidget {
    background-color: #ffffff;
    border: 2px solid #2e7d32;
    gridline-color: #2e7d32;
    selection-background-color: #a5d6a7;
    selection-color: #1b5e20;
}

/* ----- Scrollbars (Golf Ball Style) ----- */
QScrollBar:vertical {
    background: #f4e7c6;
    width: 14px;
    margin: 0;
    border-radius: 7px;
}

QScrollBar::handle:vertical {
    background: #2e7d32;
    min-height: 30px;
    border-radius: 7px;
}

QScrollBar::handle:vertical:hover {
    background: #1b5e20;
}

QScrollBar::add-line, QScrollBar::sub-line {
    height: 0;
}

/* ----- Menus ----- */
QMenuBar {
    background-color: #2e7d32;
    color: white;
}

QMenuBar::item:selected {
    background-color: #1b5e20;
}

QMenu {
    background-color: #f4e7c6;
    border: 2px solid #2e7d32;
}

QMenu::item:selected {
    background-color: #a5d6a7;
}

/* ----- GroupBox (Golf Hole Border) ----- */
QGroupBox {
    border: 2px solid #2e7d32;
    border-radius: 8px;
    margin-top: 10px;
    padding: 10px;
    font-weight: bold;
}

/* ----- ToolTips ----- */
QToolTip {
    background-color: #2e7d32;
    color: white;
    border: 1px solid #1b5e20;
    padding: 3px;
}
"""

#Set user_id to none at beginning of program

globals.user_id = None


#Start program with launching login window
class Login(QMainWindow):
    #Layout for all windows
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.setGeometry(100, 100, 500, 500)
        self.initUI()

    #UI creation
    def initUI(self):
        #Create a central widget
        cw = QWidget(self)
        self.setCentralWidget(cw)

        #Create layout plan for central widget
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(20)               
        cw.setLayout(layout)

        #Create textboxes and buttons for login page
        self.username_text = QLineEdit()
        self.username_text.setPlaceholderText("Username")
        self.password_text = QLineEdit()
        self.password_text.setPlaceholderText("Password")
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.register_page_button = QPushButton("Register")
        self.register_page_button.clicked.connect(self.register_page)

        #Add all widgets to page
        layout.addStretch()         
        layout.addWidget(self.username_text, alignment=Qt.AlignHCenter)
        layout.addWidget(self.password_text, alignment = Qt.AlignHCenter)
        layout.addWidget(self.login_button, alignment=Qt.AlignHCenter)
        layout.addWidget(self.register_page_button, alignment=Qt.AlignHCenter)
        layout.addStretch()

    #Upon login button clicked
    def login(self):
        #Get user and pass info
        username = str(self.username_text.text())
        password = str(self.password_text.text())

        #Call function in admin that hashes password
        secure_password = admin.create_secure_password(password)

        #Query database for user and pass with hash
        query = QSqlQuery()
        query.prepare("""
        SELECT user_id from users WHERE username = ? and password_hash = ?
        """)
        query.addBindValue(username)
        query.addBindValue(secure_password)
        query.exec_()

        #If query was succesful set values and create main page
        if query.next():
            globals.user_id = query.value(0)
            self.main_page = Main()
            self.main_page.show()
            self.close()
        else:
            QMessageBox.information(self, "Fail", "Username or password is incorrect")



    #Upon register button clicked
    def register_page(self):
        #Open registration page
        self.register_window = Register()
        self.register_window.show()
        self.close()

#Registration page
class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register Page")
        self.setGeometry(100, 100, 500, 500)
        self.initUI()

    def initUI(self):
        #Create central widget
        cw = QWidget(self)
        self.setCentralWidget(cw)

        #Define layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)  
        layout.setSpacing(20)               
        cw.setLayout(layout)

        #Textboxes and register
        self.username_text = QLineEdit()
        self.username_text.setPlaceholderText("Username")
        self.password_text = QLineEdit()
        self.password_text.setPlaceholderText("Password")
        self.register_page_button = QPushButton("Register")
        self.register_page_button.clicked.connect(self.register)
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back)

        #Add to layout
        layout.addStretch()         
        layout.addWidget(self.username_text, alignment=Qt.AlignHCenter)
        layout.addWidget(self.password_text, alignment = Qt.AlignHCenter)
        layout.addWidget(self.register_page_button, alignment=Qt.AlignHCenter)
        layout.addWidget(self.back_button, alignment =Qt.AlignHCenter)
        layout.addStretch()

    #On register button clicked
    def register(self):
        #Username and password from textboxes
        username = str(self.username_text.text())
        password = str(self.password_text.text())
        
        #Hash the password 
        secure_password = admin.create_secure_password(password)

        #Query database to see if username exists already
        query = QSqlQuery()
        query.prepare("""
        SELECT user_id from users WHERE username = ?
        """)
        query.addBindValue(username)
        query.exec_()
        #If it exists, show error
        if query.next():
            QMessageBox.information(self, "Error", "Username already exists, try new username or login")
        else:
            #Prepare query to add user/pass to database
            query = QSqlQuery()
            query.prepare("""
            INSERT INTO users (username, password_hash) VALUES(?, ?)
            """)
            query.addBindValue(username)
            query.addBindValue(secure_password)
            
            #If the query executes show login page
            if query.exec_():
                QMessageBox.information(self, "OK", "User Created!")
                self.login_window = Login()
                self.login_window.show()
                self.close()
            else: #Show error
                QMessageBox.warning(self, "FAIL", query.lastError().text())

    #Back button
    def back(self):
        self.login = Login()
        self.login.show()
        self.close()

#Main window class
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Page")
        self.setGeometry(100, 100, 500, 500)        
        self.initUI()

    def initUI(self):
        #Create grid for layout
        cw = QWidget(self)
        self.setCentralWidget(cw)
        grid = QGridLayout()
        cw.setLayout(grid)

        #Buttons and Sizing policies
        self.new_round_button = QPushButton()
        self.new_round_button.setMinimumHeight(50) 
        self.new_round_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.new_round_button.setText("New Round")
        self.new_round_button.clicked.connect(self.start_new_round)
        self.account_button = QPushButton()
        self.account_button.setMinimumHeight(50)
        self.account_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #Image pathing catch
        try:
            self.account_button.setIcon(QIcon(r"_pycache_\CIS 314\ai_caddy\src\ai_caddy\images"))
        finally:
            self.account_button.setText("Account")

        self.bag_button = QPushButton()
        self.bag_button.setMinimumHeight(50) 
        self.bag_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bag_button.setText("Bag")
        self.bag_button.clicked.connect(self.open_bag)
        self.display = QWidget()
        self.display.setMinimumHeight(200)
        self.display.setMinimumWidth(200)
        self.display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #Put display in a box layout
        self.display_layout = QVBoxLayout(self.display)

        #Prepare query
        #Find the round_id for the last played round of user
        query = QSqlQuery()
        query.prepare("""
            SELECT round_id
            FROM rounds
            WHERE user_id = ?
            ORDER BY round_id DESC
            LIMIT 1
        """)
        query.addBindValue(globals.user_id)
        query.exec_()

        last_round_id = None
        #If query works get the last round id
        if query.next():
            last_round_id = query.value(0)

        #Load the round data for last round played in middle of screen
        if last_round_id:
            model = QSqlQueryModel()
            model.setQuery(f"""
                SELECT s.round_id, h.hole_id, h.par, s.strokes
                FROM holes h
                JOIN scores s ON h.hole_id = s.hole_id
                WHERE s.round_id = {last_round_id}
                ORDER BY h.hole_id ASC
            """)
        else:
            model = QSqlQueryModel()
            model.setQuery("SELECT 'No previous rounds found' AS message")

        #Create table display with a scrollbar
        table = QTableView(self.display)
        table.setModel(model)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(table)
        self.display_layout.addWidget(scroll)

        #Set stretching rules for columns and rows
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setRowStretch(2, 1)
        #Add widgets to grid
        grid.addWidget(self.new_round_button, 0, 0)
        grid.addWidget(self.account_button, 0, 2)
        grid.addWidget(self.bag_button, 2, 2)
        grid.addWidget(self.display, 1, 0, 1, 3)

    #On bag button clicked, open bag
    def open_bag(self):
        self.bag_window = Bag()
        self.bag_window.show()
        self.close()
    #On round button clicked, start new round
    def start_new_round(self):
        self.new_round = NewRound()
        self.new_round.show()
        self.close()

#Start new round page
class NewRound(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Start Round Page")
        self.setGeometry(100, 100, 500, 500)
        self.initUI()

    def initUI(self):
        #Create central widget with grid 
        cw = QWidget(self)
        self.setCentralWidget(cw)
        grid = QGridLayout()
        cw.setLayout(grid)

        #Create and fill combo box with all course names
        self.course_name = QComboBox()
        query = QSqlQuery()
        query.prepare("""
            SELECT course_name FROM courses
                      """)
        query.exec_()
        #While there is a next value, add the value
        while query.next():
            course_name = query.value(0)
            self.course_name.addItem(course_name)

        # Buttons
        self.start_round_button = QPushButton("Start Round")
        self.start_round_button.clicked.connect(self.start_round)
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back)

        # Create a vertical layout to stack buttons
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.start_round_button)
        button_layout.addWidget(self.back_button)
        button_layout.addStretch()
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setRowStretch(2, 1)
        grid.addWidget(self.course_name, 1, 0)
        grid.addLayout(button_layout, 1, 2)

    def back(self):
        self.main = Main()
        self.main.show()
        self.close()

    #When start round is clicked
    def start_round(self):
        #Get the course name selected from the dropbox
        course_name = self.course_name.currentText()
        #Prepare a query that finds course id
        query = QSqlQuery()
        query.prepare("""
        SELECT course_id FROM courses WHERE course_name = ?
""")
        query.addBindValue(course_name)
        query.exec_()
        #If the query exists
        if query.next():
            #Set the global variables to the course_id
            globals.course_id = query.value(0)
            #Start new round
            self.round = Round()
            self.round.show()
            self.close()
        else:
            QMessageBox.information(self, "Error", "No course with selcted name")

#In round window
class Round(QMainWindow):
    def __init__(self):
        super().__init__()
        #Sat latitude and longitude values to none
        self.lat = None
        self.lon = None

        self.setWindowTitle("Start Round Page")
        self.setGeometry(100, 100, 500, 500)
        #Set global values to 1
        globals.current_hole = 1
        globals.score_hole = 1
        #Get global values
        user_id = globals.user_id
        course_id = globals.course_id

        #Prepare query that creates round tag
        query = QSqlQuery()
        query.prepare("""
        INSERT INTO rounds (user_id, course_id) VALUES (?, ?)                      
""")
        query.addBindValue(user_id)
        query.addBindValue(course_id)
        query.exec_()
        globals.round_id = query.lastInsertId()
        self.initUI()

    def initUI(self):
        #Create grid layout
        cw = QWidget(self)
        self.setCentralWidget(cw)
        grid = QGridLayout()
        cw.setLayout(grid)
        #Set grid spacing and margins
        grid.setContentsMargins(20, 20, 20, 20)   
        grid.setHorizontalSpacing(20)            
        grid.setVerticalSpacing(15)

        #Query database for image path name, could use blob type to get rid of folder name need
        query = QSqlQuery()
        query.prepare("""
            SELECT image
            FROM holes
            WHERE course_id = ? AND hole_id = ?
        """)
        query.addBindValue(globals.course_id)
        query.addBindValue(globals.current_hole)
        query.exec_()

        image = None
        #If query exists get the image path
        if query.next():
            image = query.value(0)

        #Set background to image of center widget
        if image:
#----------------------Maybe change to non direct file pathing------------------------------#
            folder = r"_pycache_\CIS 314\ai_caddy\src\ai_caddy\images"
            image_path = os.path.join(folder, image).replace("\\", "/")

            self.bg_pix = QPixmap(image_path)

            w, h = self.bg_pix.width(), self.bg_pix.height()
            self.resize(w, h)

            #Set background
            self.bg_label = QLabel()
            self.bg_label.setAlignment(Qt.AlignCenter)
            self.bg_label.setPixmap(
                self.bg_pix.scaled(w, h,Qt.KeepAspectRatio))
        else:
            #If it doesnt exist, say no image
            self.bg_label = QLabel("No Image")
            self.bg_label.setAlignment(Qt.AlignCenter)
            self.bg_label.setStyleSheet("background: gray;")

        #Left sidebar, using fixed widths
        left_sidebar = QWidget()
        left_sidebar.setFixedWidth(350)
        left_layout = QVBoxLayout(left_sidebar)

        #Add hole info, next button, and get distance to left sidebar
        self.hole_info = QLabel(f"Hole: {globals.current_hole}")
        self.next_hole_button = QPushButton("Next Hole and Enter Score")
        self.next_hole_button.clicked.connect(self.next_hole)
        self.distance_label = QLabel("Distance to hole in yards: ")
        self.mid_green_distance_button = QPushButton("Get distance to middle green.")
        self.mid_green_distance_button.clicked.connect(self.distance_to_hole)
        self.end_round_button = QPushButton("End Round")
        self.end_round_button.clicked.connect(self.end_round)

        #Add to left layouts
        left_layout.addWidget(self.hole_info)
        left_layout.addWidget(self.next_hole_button)
        left_layout.addWidget(self.distance_label)
        left_layout.addWidget(self.mid_green_distance_button)
        left_layout.addWidget(self.end_round_button)
        left_layout.addStretch()


        #Right sidebar
        right_sidebar = QWidget()
        right_sidebar.setFixedWidth(350)
        right_layout = QVBoxLayout(right_sidebar)

        #Add caddy button, response, pin asker, and gps
        self.caddy_response = QLabel("Caddy Response:")
        self.caddy_response.setWordWrap(True)
        self.pin_location = QComboBox()
        self.pin_location.addItem("Front")
        self.pin_location.addItem("Middle")
        self.pin_location.addItem("Back")
        self.ask_caddy_button = QPushButton("Ask Caddy")
        self.ask_caddy_button.clicked.connect(self.ask_caddy)
        self.gps_label = QLabel("GPS: (not retrieved)")
        self.gps_label.setWordWrap(True)

        #Add to right layout
        right_layout.addWidget(self.pin_location)
        right_layout.addWidget(self.ask_caddy_button)
        right_layout.addWidget(self.caddy_response)
        right_layout.addWidget(self.gps_label)
        right_layout.addStretch()

        #Add left, center, right, to grid
        grid.addWidget(left_sidebar, 0, 0, 3, 1)   
        grid.addWidget(self.bg_label, 0, 1, 3, 1)
        grid.addWidget(right_sidebar, 0, 2, 3, 1)
        #Column stretching
        grid.setColumnStretch(0, 0) 
        grid.setColumnStretch(1, 1) 
        grid.setColumnStretch(2, 0)

    #On asking caddy clicked
    def ask_caddy(self):
        #Query for golf clubs of user 
        query = QSqlQuery()
        query.prepare("""
        SELECT * FROM bags WHERE user_id = ?
""")    
        query.addBindValue(globals.user_id)
        query.exec_()
        user_bag = []

        #Fill bag to use for asking chatgpt club recommendation
        while query.next():
            club = {
                "Club": query.value(2), 
                "Distance": query.value(3)
            }
            user_bag.append(club)
        
        #Fill hole info to use with chatgpt
        query = QSqlQuery()
        query.prepare("""
        SELECT * FROM holes WHERE course_id = ? and hole_id = ?
""")
        query.addBindValue(globals.course_id)
        query.addBindValue(globals.current_hole)
        query.exec_()

        hole_info = []

        if query.next():
            info = {"Par":  query.value(1),
                   "Description": query.value(2) 
            }
            hole_info.append(info)

        #If the latitude and longitude values are not None
        if self.lat and self.lon:
            #Use lat and lon values to ask chat gpt for club recommendation
            distance = self.distance_label.text()
            self.caddy_response.setText(golf_ai.ask_chat(user_bag, hole_info, distance))
            #Reset lat/lon to None for making sure location gets updated
            self.lat = None
            self.lon = None
        else:
            #Prompt user to click update location to use chat function
            self.caddy_response.setText("Please update user location first.")

    #On next hole button clicked
    def next_hole(self):
        #Prompt user to enter score for last hole
        self.enter_score = EnterScore()
        self.enter_score.show()
        #If the current hole is still less than 19, go to next hole
        if globals.current_hole < 19:
            globals.current_hole += 1                
            self.initUI()

    #On end round button clicked
    def end_round(self):
        #Fill all leftover holes with 0 to keep consistency in database
        while globals.current_hole < 18:
            query = QSqlQuery()
            query.prepare(""" 
            INSERT INTO scores (round_id, hole_id, strokes) VALUES (?, ?, ?)
            """)
            
            query.addBindValue(globals.round_id)
            query.addBindValue(globals.current_hole)
            query.addBindValue(0)
            query.exec_()
            globals.current_hole +=1

        #Go back to main window
        self.main_window = Main()
        self.main_window.show()
        self.close()

        #-------------ADD Function-----------------#
        #Show round info when hole id is 19

    #Get location function
    def get_location(self):
        #Attempt to use devices gps device to create connection
        self.source = QGeoPositionInfoSource.createDefaultSource(self)
            #If no gps, return that there is none available
        if not self.source:
            self.gps_label.setText("GPS Not Available on this device.")
            return
        #Otherwise, start making gps connection calls
        self.source.positionUpdated.connect(self.position_updated)
        self.source.startUpdates()

    #Position updating function called by get_location
    def position_updated(self, position):
        #Get lat/lon values
        self.lat = position.coordinate().latitude()
        self.lon = position.coordinate().longitude()
        self.gps_label.setText(f"Latitude: {self.lat}\nLongitude: {self.lon}")

        #Stop continuous source of updates
        self.source.stopUpdates()

        #If position object has lat and lon values
        if hasattr(self, 'hole_lat') and hasattr(self, 'hole_lon'):
            #Get tuples of hole and user coordinates
            hole_cords = (self.hole_lat, self.hole_lon)
            user_cords = (self.lat, self.lon)
            #Compute distance using geopy, in meters
            distance_m = distance(hole_cords, user_cords)
            #Convert to yards and set text
            distance_y = distance_m.m * 1.0936
            self.distance_label.setText(str(distance_y) + " yards")

    #Calculate distance to hole function, uses position_updated
    def distance_to_hole(self):
        #Query to get lat, lon values from current hole
        query = QSqlQuery()
        query.prepare("SELECT lat, lon FROM holes WHERE hole_id = ?")
        query.addBindValue(globals.current_hole)
        query.exec_()

        #If no query, say no coordinates found
        if not query.next():
            self.distance_label.setText("Hole coordinates not found.")
            return

        hole_lat = query.value(0)
        hole_lon = query.value(1)

        #If no coords, declare no coords
        if hole_lat is None or hole_lon is None:
            self.distance_label.setText("Hole GPS coordinates not available.")
            return

        #Store self lat and lon values in object
        self.hole_lat = hole_lat
        self.hole_lon = hole_lon

        #Ask gps to update
        self.get_location()
        #Tell user that gps is locating
        self.distance_label.setText("Getting GPS location...")
        
#Enter score window
class EnterScore(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Score Page: ")
        self.setGeometry(100, 100, 300, 300)
        self.initUI()

    def initUI(self):
        #Set grid layout
        cw = QWidget(self)
        self.setCentralWidget(cw)
        grid = QGridLayout()
        cw.setLayout(grid)

        #Submit button and create combo box
        self.submit_score_button = QPushButton("Submit Strokes")
        self.submit_score_button.clicked.connect(self.submit_score)
        self.enter_score = QComboBox()
        for i in range(1, 11):
            self.enter_score.addItem(str(i))
        
        grid.addWidget(self.enter_score, 0,0)
        grid.addWidget(self.submit_score_button, 1, 0)

    #On submit button clicked
    def submit_score(self):
        #Get text from combo box
        strokes = self.enter_score.currentText()
        #Prepare query to add to combo box
        query = QSqlQuery()
        query.prepare(""" 
        INSERT INTO scores (round_id, hole_id, strokes) VALUES (?, ?, ?)
        """)
        
        query.addBindValue(globals.round_id)
        query.addBindValue(globals.score_hole)
        query.addBindValue(strokes)
        query.exec_()
        #Increment scoring hole
        globals.score_hole += 1 
        self.close()

#Bag class window 
class Bag(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bag Page")
        self.setGeometry(100, 100, 500, 500)
        self.initUI()

    def initUI(self):
        #Set grid layout
        cw = QWidget(self)
        self.setCentralWidget(cw)
        grid = QGridLayout()
        cw.setLayout(grid)

        #Display current user bag with tableview
        self.display_bag = QWidget()
        self.display_layout = QVBoxLayout(self.display_bag)
        self.model = QSqlTableModel()
        self.model.setTable("bags")
        self.model.setFilter(f"user_id = {globals.user_id}")
        self.model.select()
        table = QTableView(self.display_bag)
        table.setModel(self.model)
        self.display_layout.addWidget(table)

        #Entering new club and distance
        self.club_choice = QLineEdit()
        self.club_choice.setPlaceholderText("Enter which club")
        self.club_distance = QLineEdit()
        self.club_distance.setPlaceholderText("Average Carry Distance")
        self.add_club_button = QPushButton()
        self.add_club_button.setText("Add Club")
        self.add_club_button.clicked.connect(self.add_club)

        #Back button to main menu
        self.back_button = QPushButton()
        self.back_button.setText("Back")
        self.back_button.clicked.connect(self.back)

        #Column rules
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setRowStretch(2, 1)
        grid.addWidget(self.display_bag, 0, 0, 1, 3)
        grid.addWidget(self.add_club_button, 1, 2)
        grid.addWidget(self.back_button, 2, 1)
        grid.addWidget(self.club_choice, 1, 0)
        grid.addWidget(self.club_distance, 1, 1)

    #On add club clicked
    def add_club(self):
        #Get club and distance text
        club = str(self.club_choice.text())
        distance = int(self.club_distance.text())

        #Prepare query to insert into bags
        query = QSqlQuery()
        query.prepare("""
        INSERT INTO bags (user_id, club, distance) VALUES (?, ?, ?)
                      """)
        query.addBindValue(globals.user_id)
        query.addBindValue(club)
        query.addBindValue(distance)
        query.exec_()

        #Re-display model with new club
        self.model.setTable("bags")
        self.model.setFilter(f"user_id = {globals.user_id}")
        self.model.select()
        table = QTableView(self.display_bag)
        table.setModel(self.model)
        self.model.select()

    #On back button clicked, go to main menu
    def back(self):
        self.main_window = Main()
        self.main_window.show()
        self.close()

#Create database with qsqlite
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("golf.db")
if not database.open():
    QMessageBox.critical(None, "Error", "Could not open your database")
    sys.exit(1)

#Create tables with foreign keys for database, if not exists
query = QSqlQuery()
query.exec_("PRAGMA foreign_keys = ON;")

query.exec_("""
            CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL
);
""")

query.exec_("""
CREATE TABLE IF NOT EXISTS courses( 
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT UNIQUE NOT NULL
);
""")

query.exec_("""
CREATE TABLE IF NOT EXISTS rounds(
    round_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(course_id) REFERENCES courses(course_id)

);
""")

query.exec_("""CREATE TABLE IF NOT EXISTS holes (
    hole_id INTEGER PRIMARY KEY AUTOINCREMENT,
    par INTEGER NOT NULL,
    description TEXT,
    lat REAL,
    lon REAL,
    course_id INTEGER,
    image TEXT,
    FOREIGN KEY(course_id) REFERENCES courses(course_id));
"""
)

query.exec_("""CREATE TABLE IF NOT EXISTS scores (
    score_id INTEGER PRIMARY KEY AUTOINCREMENT,
    round_id INTEGER NOT NULL,
    hole_id INTEGER NOT NULL,
    strokes INTEGER NOT NULL,
    FOREIGN KEY(round_id) REFERENCES rounds(round_id),
    FOREIGN KEY(hole_id) REFERENCES holes(hole_id)
);
""")

query.exec_("""
CREATE TABLE IF NOT EXISTS bags(
    bag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    club VARCHAR(50) NOT NULL,
    distance INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);
""")

if __name__  == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(GOLFSHEET)
    window = Login()
    window.show()
    sys.exit(app.exec())
        