import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QWidget, QVBoxLayout, QMessageBox, QGridLayout, QSizePolicy, QComboBox, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QTableView
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtGui import QIcon, QPixmap
import globals, admin, golf_ai

globals.user_id = None

class Login(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login Page")
        self.setGeometry(100, 100, 500, 500)

        self.initUI()

    def initUI(self):

        cw = QWidget(self)
        self.setCentralWidget(cw)

        # Vertical layout (centered)
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)  # remove left/right padding if desired
        layout.setSpacing(20)               # vertical spacing between items
        cw.setLayout(layout)

        self.username_text = QLineEdit()
        self.username_text.setPlaceholderText("Username")

        self.password_text = QLineEdit()
        self.password_text.setPlaceholderText("Password")

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        self.register_page_button = QPushButton("Register")
        self.register_page_button.clicked.connect(self.register_page)

        # add widgets
        layout.addStretch()         
        layout.addWidget(self.username_text, alignment=Qt.AlignHCenter)
        layout.addWidget(self.password_text, alignment = Qt.AlignHCenter)
        layout.addWidget(self.login_button, alignment=Qt.AlignHCenter)
        layout.addWidget(self.register_page_button, alignment=Qt.AlignHCenter)
        layout.addStretch()

    def login(self):
        username = self.username_text.text()
        password = self.password_text.text()

        secure_password = admin.create_secure_password(password)

        #Reverse hash
        query = QSqlQuery()
        query.prepare("""
        SELECT user_id from users WHERE username = ? and password_hash = ?
        """)
        query.addBindValue(username)
        query.addBindValue(secure_password)
        query.exec_()

        if query.next():
            print("Success")
            globals.user_id = query.value(0)
            print(globals.user_id)
            self.main_page = Main()
            self.main_page.show()
            self.close()
        else:
            print("Not in users list")

    def register_page(self):
        self.register_window = Register()
        self.register_window.show()
        self.close()

class Register(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Register Page")
        self.setGeometry(100, 100, 500, 500)
        self.initUI()

    def initUI(self):
        cw = QWidget(self)
        self.setCentralWidget(cw)

        # Vertical layout (centered)
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)  # remove left/right padding if desired
        layout.setSpacing(20)               # vertical spacing between items
        cw.setLayout(layout)

        self.username_text = QLineEdit()
        self.username_text.setPlaceholderText("Username")

        self.password_text = QLineEdit()
        self.password_text.setPlaceholderText("Password")

        self.register_page_button = QPushButton("Register")
        self.register_page_button.clicked.connect(self.register)

        # add widgets
        layout.addStretch()         
        layout.addWidget(self.username_text, alignment=Qt.AlignHCenter)
        layout.addWidget(self.password_text, alignment = Qt.AlignHCenter)
        layout.addWidget(self.register_page_button, alignment=Qt.AlignHCenter)
        layout.addStretch()

    def register(self):
        #Store the login information, user/pass in the database
        username = self.username_text.text()
        password = self.password_text.text()

        secure_password = admin.create_secure_password(password)

        query = QSqlQuery()
        query.prepare("""
        INSERT INTO users (username, password_hash) VALUES(?, ?)
        """)
        query.addBindValue(username)
        query.addBindValue(secure_password)
        
        if query.exec_():   # execute and check
            QMessageBox.information(self, "OK", "User Created!")
            self.login_window = Login()
            self.login_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "FAIL", query.lastError().text())


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Page")
        self.setGeometry(100, 100, 500, 500)        
        self.initUI()

    def initUI(self):
        cw = QWidget(self)
        self.setCentralWidget(cw)

        grid = QGridLayout()
        cw.setLayout(grid)

        self.new_round_button = QPushButton()
        self.new_round_button.setMinimumHeight(50) 
        self.new_round_button.setSizePolicy(
    QSizePolicy.Expanding,   # width grow
    QSizePolicy.Expanding    # height grow
)
        self.new_round_button.setText("New Round")
        self.new_round_button.clicked.connect(self.start_new_round)
    
        self.account_button = QPushButton()
        self.account_button.setMinimumHeight(50)
        self.account_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.account_button.setIcon(QIcon(r"C:\Users\pholl\OneDrive\Desktop\_pycache_\CIS 314\golf_app\images\account_icon.png"))


        self.bag_button = QPushButton()
        self.bag_button.setMinimumHeight(50) 
        self.bag_button.setSizePolicy(
    QSizePolicy.Expanding,   # width grow
    QSizePolicy.Expanding    # height grow
        )
        self.bag_button.setText("Bag")
        self.bag_button.clicked.connect(self.open_bag)

        self.display = QWidget()
        self.display.setMinimumHeight(200)
        self.display.setMinimumWidth(200)
        self.display.setSizePolicy(
    QSizePolicy.Expanding,   # width grow
    QSizePolicy.Expanding    # height grow
        )

        self.display_layout = QVBoxLayout(self.display)

        model = QSqlTableModel()
        model.setTable("holes")
        model.select()
        table = QTableView(self.display)
        table.setModel(model)

        self.display_layout.addWidget(table)


        #set stretching of grid
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)

        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setRowStretch(2, 1)

        grid.addWidget(self.new_round_button, 0, 0)
        grid.addWidget(self.account_button, 0, 2)
        grid.addWidget(self.bag_button, 2, 2)
        grid.addWidget(self.display, 1, 0, 1, 3)

    def open_bag(self):
        self.bag_window = Bag()
        self.bag_window.show()
        self.close()

    def start_new_round(self):
        self.new_round = NewRound()
        self.new_round.show()
        self.close()

class NewRound(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Start Round Page")
        self.setGeometry(100, 100, 500, 500)

        self.initUI()

    def initUI(self): 
        cw = QWidget(self)
        self.setCentralWidget(cw)

        grid = QGridLayout()
        cw.setLayout(grid)

        self.course_name = QComboBox()
        query = QSqlQuery()
        query.prepare("""
            SELECT course_name FROM courses
                      """)
        query.exec_()
        while query.next():
            course_name = query.value(0)
            self.course_name.addItem(course_name)
            print(course_name)


        self.start_round_button = QPushButton()
        self.start_round_button.setText("Start Round")
        self.start_round_button.clicked.connect(self.start_round)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setRowStretch(2, 1)

        grid.addWidget(self.course_name, 1, 0)
        grid.addWidget(self.start_round_button, 1, 2)

    def start_round(self):
        course_name = self.course_name.currentText()
        query = QSqlQuery()
        query.prepare("""
        SELECT course_id FROM courses WHERE course_name = ?
""")
        query.addBindValue(course_name)
        query.exec_()
        print(course_name)

        if query.next():
            globals.course_id = query.value(0)
            print(f"Loaded course_id: {globals.course_id}")
        
            self.round = Round()
            self.round.show()
            self.close()
        else:
            print("No course found with that name.")

class Round(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Start Round Page")
        self.setGeometry(100, 100, 500, 500)
        globals.current_hole = 1
        globals.score_hole = 1
        user_id = globals.user_id
        course_id = globals.course_id

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
        cw = QWidget(self)
        self.setCentralWidget(cw)

        grid = QGridLayout()
        cw.setLayout(grid)

        # --- Query DB for image ---
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
        if query.next():
            image = query.value(0)

        # --- Set background using QLabel (not stylesheet) ---
        if image:
            folder = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\CIS 314\golf_app\images"
            image_path = os.path.join(folder, image).replace("\\", "/")

            self.bg_pix = QPixmap(image_path)

            # Resize window slightly larger than image
            w, h = self.bg_pix.width(), self.bg_pix.height()
            self.resize(w + 300, h)

            # Create background label
            self.bg_label = QLabel(cw)
            self.bg_label.setGeometry(0, 0, self.width(), self.height())
            self.bg_label.setAlignment(Qt.AlignCenter)
            self.bg_label.setPixmap(
                self.bg_pix.scaled(
                    self.bg_label.size(),
                         Qt.KeepAspectRatio
                )
            )
            self.bg_label.lower()  # push behind everything
        else:
            cw.setStyleSheet("QWidget { background-color: gray; }")

        # --- UI Widgets (always on top) ---
        self.hole_info = QLabel(f"Hole: {globals.current_hole}")
        self.next_hole_button = QPushButton("Next Hole")
        self.next_hole_button.clicked.connect(self.next_hole)
        self.caddy_response = QLabel("Caddy Response: ")
        self.ask_caddy_button = QPushButton("Ask Caddy: ")
        self.ask_caddy_button.clicked.connect(self.ask_caddy)

        self.ask_distance = QLineEdit("Enter distance to hole and pin location:")

        # Stack vertically in same column
        grid.addWidget(self.caddy_response, 0 ,1)
        grid.addWidget(self.ask_caddy_button, 2, 1)
        grid.addWidget(self.hole_info, 0, 0)
        grid.addWidget(self.next_hole_button, 1, 0)
        grid.addWidget(self.ask_distance, 1, 1)

        # Raise widgets in front of background
        self.hole_info.raise_()
        self.next_hole_button.raise_()

    def ask_caddy(self):
        query = QSqlQuery()
        query.prepare("""
        SELECT * FROM bags WHERE user_id = ?
""")    
        query.addBindValue(globals.user_id)
        query.exec_()

        user_bag = []

        while query.next():
            club = {
                "Club": query.value(2), 
                "Distance": query.value(3)
            }
            user_bag.append(club)
        print(user_bag)

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
        print(hole_info)



        #Right now ask user to input distance to hole
        #Later want gps functoin to auto get distances        
        distances = self.ask_distance.text()
        self.caddy_response.setText(golf_ai.ask_chat(user_bag, hole_info, distances))

    def next_hole(self):
        self.enter_score = EnterScore()
        self.enter_score.show()
        #Wait until EnterScore is closed
        if globals.current_hole < 19:
            globals.current_hole = globals.current_hole + 1
            self.initUI()
        else:
            self.end_round()
    
    def end_round(self):
        pass

class EnterScore(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Score Page: ")
        self.setGeometry(100, 100, 300, 300)

        self.initUI()

    def initUI(self):
        cw = QWidget(self)
        self.setCentralWidget(cw)

        grid = QGridLayout()
        cw.setLayout(grid)

        self.submit_score_button = QPushButton("Submit Strokes")
        self.submit_score_button.clicked.connect(self.submit_score)
        self.enter_score = QComboBox()
        for i in range(1, 11):
            self.enter_score.addItem(str(i))
        
        grid.addWidget(self.enter_score, 0,0)
        grid.addWidget(self.submit_score_button, 1, 0)

    def submit_score(self):
        
        strokes = self.enter_score.currentText()

        query = QSqlQuery()
        query.prepare(""" 
        INSERT INTO scores (round_id, hole_id, strokes) VALUES (?, ?, ?)
        """)
        
        query.addBindValue(globals.round_id)
        query.addBindValue(globals.score_hole)
        query.addBindValue(strokes)
        query.exec_()

        globals.score_hole += 1

        self.close()

class Bag(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bag Page")
        self.setGeometry(100, 100, 500, 500)

        self.initUI()

    def initUI(self):
        cw = QWidget(self)
        self.setCentralWidget(cw)

        grid = QGridLayout()
        cw.setLayout(grid)

        self.display_bag = QWidget()
        self.display_layout = QVBoxLayout(self.display_bag)

        self.model = QSqlTableModel()
        self.model.setTable("bags")
        self.model.setFilter(f"user_id = {globals.user_id}")
        self.model.select()
        table = QTableView(self.display_bag)
        table.setModel(self.model)

        self.display_layout.addWidget(table)

        self.club_choice = QLineEdit()
        self.club_choice.setPlaceholderText("Enter which club")
        self.club_distance = QLineEdit()
        self.club_distance.setPlaceholderText("Average Carry Distance")


        self.add_club_button = QPushButton()
        self.add_club_button.setText("Add Club")
        self.add_club_button.clicked.connect(self.add_club)

        self.back_button = QPushButton()
        self.back_button.setText("Back")
        self.back_button.clicked.connect(self.back)

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

    #Open window and add new club, then close window
    def add_club(self):
        print("Insert")
        club = str(self.club_choice.text())
        distance = int(self.club_distance.text())

        query = QSqlQuery()
        query.prepare("""
        INSERT INTO bags (user_id, club, distance) VALUES (?, ?, ?)
                      """)
        query.addBindValue(globals.user_id)
        query.addBindValue(club)
        query.addBindValue(distance)
        query.exec_()

        self.model.setTable("bags")
        self.model.setFilter(f"user_id = {globals.user_id}")
        self.model.select()
        table = QTableView(self.display_bag)
        table.setModel(self.model)

        self.model.select()

    def back(self):
        self.main_window = Main()
        self.main_window.show()
        self.close()

#Database creation
database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("golf.db")
if not database.open():
    QMessageBox.critical(None, "Error", "Could not open your database")
    sys.exit(1)


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

query.exec_("""
CREATE TABLE IF NOT EXISTS holes(
    hole_id INTEGER PRIMARY KEY AUTOINCREMENT,
    par INTEGER NOT NULL,
    desc TEXT,
    front_green TEXT,
    middle_green TEXT,
    back_green TEXT,
    course_id INTEGER,
    image TEXT,
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
);

""")

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
    window = Login()
    window.show()
    sys.exit(app.exec())
