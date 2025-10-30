import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QWidget
from PyQt5.QtCore import QSize

#Style Sheets from ChatGPT

DARK_APP_STYLE = """
    QWidget {
        background-color: #1e1e2f;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        color: #e4e4e4;
    }

    QLineEdit {
        background-color: #2a2a3b;
        border: 2px solid #3d3d55;
        border-radius: 8px;
        padding: 8px;
        color: #ffffff;
        selection-background-color: #0a84ff;
    }

    QLineEdit:focus {
        border: 2px solid #0a84ff;
        background-color: #2f2f42;
    }

    QPushButton {
        background-color: #0a84ff;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
    }

    QPushButton:hover {
        background-color: #006fd6;
    }

    QPushButton:pressed {
        background-color: #005bb5;
    }

    QMainWindow {
        background-color: #1e1e2f;
    }
"""

LIGHT_APP_STYLE = """
    QWidget {
        background-color: #f5f7fa;
        font-family: 'Segoe UI', sans-serif;
        font-size: 14px;
        color: #2e3b4e;
    }

    QLineEdit {
        background-color: #ffffff;
        border: 2px solid #d1d9e6;
        border-radius: 8px;
        padding: 8px;
        selection-background-color: #0078d7;
    }

    QLineEdit:focus {
        border: 2px solid #0078d7;
        background-color: #f9fcff;
    }

    QPushButton {
        background-color: #0078d7;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
    }

    QPushButton:hover {
        background-color: #005a9e;
    }

    QPushButton:pressed {
        background-color: #004578;
    }

    QMainWindow {
        background-color: #f5f7fa;
    }

    QWidget#NewWindow {
        background-color: #fdfdfd;
    }
"""


#Class for first main window

class MainWindow(QMainWindow):
    def __init__(self, color): #Takes color for style sheets
        super().__init__()
    
        #Creating first window
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 500, 500)
        #Pointer for next window opened
        self.new_window = None
        self.color = color
        self.initUI()


    def initUI(self): #Build function
        #Set style sheet based on color
        self.setStyleSheet(self.color)

        #Make textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(100, 100)
        self.textbox.resize(280, 40)
        self.textbox.setPlaceholderText("Enter something...")
        
        #Make submit button
        self.button = QPushButton("Submit", self)
        self.button.setFixedSize(QSize(100, 40))
        self.button.move(200, 160)
        self.button.clicked.connect(self.on_click)

        #Make color toggle button
        self.toggle = QPushButton("Change Color", self)
        self.toggle.setFixedSize(QSize(140, 40))
        self.toggle.move(180, 220)
        self.toggle.clicked.connect(self.on_toggle)

    #On Submit function
    def on_click(self):
        #Get the text from the textbox
        text = self.textbox.text()
        #Get current color
        color = self.color
        #Create the new window that keeps the text in the new textbox and displays it as the title of the next window
        self.new_window = NewWindow(text, color)
        #Show new window
        self.new_window.show()
        #Close old window
        self.close()
    
    #Button for toggling light and dark color style
    def on_toggle(self):
        if self.color == LIGHT_APP_STYLE:
            self.color = DARK_APP_STYLE
        else:
            self.color = LIGHT_APP_STYLE
        self.setStyleSheet(self.color)

#New window class
class NewWindow(QWidget):
    #Accepts text from textbox and previous window color mode
    def __init__(self, text_passed, color):
        super().__init__()
        self.text_passed = text_passed
        #Set window title to old textbox text
        self.setWindowTitle(str(text_passed))
        self.setGeometry(100, 100, 500, 500)
        self.color = color
        self.initUI()

    #Builder function
    def initUI(self):
        self.setStyleSheet(self.color)

        #Make textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(100, 100)
        self.textbox.resize(280, 40)
        self.textbox.setText(self.text_passed)

        #Make button
        self.button = QPushButton("Submit Again", self)
        self.button.setFixedSize(QSize(120, 60))
        self.button.move(200, 160)
        self.button.clicked.connect(self.on_click)

        #Make toggle button
        self.toggle = QPushButton("Change Color", self)
        self.toggle.setFixedSize(QSize(140, 40))
        self.toggle.move(180, 220)
        self.toggle.clicked.connect(self.on_toggle)

    #On submit function
    def on_click(self):
        text = self.textbox.text()
        color = self.color
        self.new_window = NewWindow(text, color)
        self.new_window.show()
        self.close()

    #On toggle button
    def on_toggle(self):
        if self.color == LIGHT_APP_STYLE:
            self.color = DARK_APP_STYLE
        else:
            self.color = LIGHT_APP_STYLE
        self.setStyleSheet(self.color)

#PyQt5 start 
app = QApplication(sys.argv)
window = MainWindow(DARK_APP_STYLE)
window.show()
sys.exit(app.exec())