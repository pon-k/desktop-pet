import os, sys, tkinter
from pathlib import Path
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PySide6.QtGui import QMovie
from PySide6 import QtCore
from dotenv import load_dotenv
import random

# Fetch screen resolution

scr = tkinter.Tk()
width = scr.winfo_screenwidth()
height = scr.winfo_screenheight()

# Fetch filepaths

load_dotenv()
BLINK_R, BLINK_L = os.getenv("BLINK_R"), os.getenv("BLINK_L")
RUN_R, RUN_L = os.getenv("RUN_R"), os.getenv("RUN_L")
WAG_R, WAG_L = os.getenv("WAG_R"), os.getenv("WAG_L")


# Assign variables and such

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.window = QWidget()
        self.setWindowTitle('SIR ALARIC THE NOBLE')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(width * 0.7, height * 0.7, 200, 200)
        self.setFixedSize(200, 200)
        self.label = QLabel()
        self.movie = QMovie(BLINK_R)
        self.label.setMovie(self.movie)
        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)
        self.movie.start()
    
    def switch_sprite(self, sprite):
        self.movie.stop()
        self.label.clear()
        self.label = QLabel()
        self.movie = QMovie(sprite)
        self.label.setMovie(self.movie)
        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)
        self.movie.start()

    def running(self):
        roll = random.randrange(0,1)
        if roll == 0:
            



app = QApplication(sys.argv)
main = MainWindow()
main.show()
app.exec()



