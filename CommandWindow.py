from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class CommandWindow:
    def __init__(self):
        self.sizeHint = lambda: QSize(1280, 900)
        self.move(100, 10)
        self.mainFrame = QFrame()
        self.setCentralWidget(self.mainFrame)
        t_lay_parent = QHBoxLayout()
        t_lay_parent.setContentsMargins(0, 0, 0, 0)

        self.videoFrame = QFrame()
        self.videoFrame.mouse_double_click_event = self.mouse_double_click_event
        t_lay_parent.addWidget(self.videoFrame)
        self.show()

    def mouse_double_click_event(self, event):
        if event.button() == Qt.LeftButton:
            if self.windowState() == Qt.WindowNoState:
                self.videoFrame.show()
                self.setWindowState(Qt.WindowFullScreen)
            else:
                self.setWindowState(Qt.WindowNoState)

    def mouse_double_click_event1(self, event):
        if event.button() == Qt.LeftButton:
            if self.windowState() == Qt.WindowNoState:
                self.videoFrame.hide()
                self.setWindowState(Qt.WindowFullScreen)
            else:
                self.videoFrame.show()
                self.setWindowState(Qt.WindowNoState)

