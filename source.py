import sys
import vlc
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.sizeHint = lambda: QSize(250, 100)
        self.move(100, 50)
        wid = QWidget(self)
        self.setCentralWidget(wid)
        layout = QVBoxLayout()
        _1stHLayout = QHBoxLayout()
        _1stHLayout.addWidget(QLineEdit())
        _1stHLayout.addWidget(QPushButton('اتصال'))
        layout.addLayout(_1stHLayout)
        _2ndHLayout = QHBoxLayout()
        _2ndHLayout.addWidget(QPushButton('به اشتراکم بگذار'))
        layout.addLayout(_2ndHLayout)
        wid.setLayout(layout)
        self.show()


class StreamWindow:
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
        self.vlcInstance = vlc.Instance(['--video-on-top'])
        self.videoPlayer = self.vlcInstance.media_player_new()
        self.videoPlayer = self.vlcInstance.media_player_new()
        self.videoPlayer.video_set_mouse_input(False)
        self.videoPlayer.video_set_key_input(False)
        self.videoPlayer.set_mrl("rtsp://serveo.net:42432/test", "network-caching=300")
        self.videoPlayer.audio_set_mute(True)
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.videoPlayer.set_xwindow(self.videoFrame.winId())
        elif sys.platform == "win32": # for Windows
            self.videoPlayer.set_hwnd(self.videoFrame.winId())
        elif sys.platform == "darwin": # for MacOS
            self.videoPlayer.set_nsobject(int(self.videoFrame.winId()))

        self.videoPlayer.play()

        self.mainFrame.setLayout(t_lay_parent)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("IR.DS")

    window = MainWindow()
    app.exec_()
