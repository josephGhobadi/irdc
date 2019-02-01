import sys

from PyQt5.QtWidgets import *
from mainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("IR.DS")

    window = MainWindow()
    app.exec_()
