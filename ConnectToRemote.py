from PyQt5.QtWidgets import *


class ConnectToRemote:
    def __init__(self, remote_address):
        alert = QMessageBox()
        alert.setText("To Do!" + remote_address)
        alert.exec_()


