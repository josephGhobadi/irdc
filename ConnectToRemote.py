import sys
import vlc

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# TODO : webSocket get remote screen size, other things


class ConnectToRemote(QMainWindow):
    def __init__(self, parent, remote_address):
        super(ConnectToRemote, self).__init__(parent)
        # ensure this window gets garbage-collected when closed
        self.setAttribute(Qt.WA_DeleteOnClose)

        # servers attributes
        [self.rtsp_port, self.command_port] = remote_address.split(":")
        self.server_address = "serveo.net"

        # None objects
        self.sizeHint = None
        self.mainFrame = None
        self.videoFrame = None
        self.vlcInstance = None
        self.videoPlayer = None

        # function calls
        self.draw_command_window()

    def draw_command_window(self):
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
        self.videoPlayer.set_mrl("rtsp://" + self.server_address + ":" + self.rtsp_port + "/test", "network-caching=100")
        self.videoPlayer.audio_set_mute(True)
        if sys.platform.startswith('linux'):  # for Linux using the X Server
            self.videoPlayer.set_xwindow(self.videoFrame.winId())
        elif sys.platform == "win32":  # for Windows
            self.videoPlayer.set_hwnd(self.videoFrame.winId())
        elif sys.platform == "darwin":  # for MacOS
            self.videoPlayer.set_nsobject(int(self.videoFrame.winId()))

        self.videoPlayer.play()

        self.mainFrame.setLayout(t_lay_parent)
        self.show()

    def mouse_double_click_event(self, event):
        # FIXME complete this
        pass

    def mouse_double_click_event1(self, event):
        # FIXME complete this
        pass

    def closeEvent(self, QCloseEvent):
        self.close()
        self.parent().show()
