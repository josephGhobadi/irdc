import sys
import json
import threading

import websockets
import vlc
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ConnectToRemote(QMainWindow):
    def __init__(self, parent, remote_address):
        self.mouse_press_x = None
        self.mouse_press_y = None
        self.mouse_release_x = None
        self.mouse_release_y = None
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

        # websocket
        self.websocket = websockets.connect('ws://' + self.server_address + ':' + self.command_port)

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
        self.videoFrame.mousePressEvent = self.mouse_press_event
        self.videoFrame.mouseReleaseEvent = self.mouse_release_event
        self.videoFrame.keyPressEvent = self.keyboard_press_event
        self.videoFrame.keyReleaseEvent = self.keyboard_release_event
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

    def websocket_send(self, obj):
        self.websocket.send(obj)

    def mouse_press_event(self, event):
        obj = ""
        if event.buttons() & Qt.LeftButton:
            obj = json.JSONEncoder().encode({
                "command": "mouse_press", "params": {"button": "left", "x": event.pos().x(), "y": event.pos().y()}
            })
        elif event.buttons() & Qt.RightButton:
            obj = json.JSONEncoder().encode({
                "command": "mouse_press", "params": {"button": "Right", "x": event.pos().x(), "y": event.pos().y()}
            })

        t = threading.Thread(target=self.websocket_send, args=obj)
        t.start()

    def mouse_release_event(self, event):
        obj = ""
        if event.buttons() & Qt.LeftButton:
            obj = json.JSONEncoder().encode({
                "command": "mouse_release", "params": {"button": "left", "x": event.pos().x(), "y": event.pos().y()}
            })
        elif event.buttons() & Qt.RightButton:
            obj = json.JSONEncoder().encode({
                "command": "mouse_release", "params": {"button": "Right", "x": event.pos().x(), "y": event.pos().y()}
            })

        t = threading.Thread(target=self.websocket_send, args=obj)
        t.start()

    def keyboard_press_event(self, event):
        obj = json.JSONEncoder().encode({
            "command": "keyboard_press", "code": event.key()
        })

        t = threading.Thread(target=self.websocket_send, args=obj)
        t.start()

    def keyboard_release_event(self, event):
        obj = json.JSONEncoder().encode({
            "command": "keyboard_release", "code": event.key()
        })

        t = threading.Thread(target=self.websocket_send, args=obj)
        t.start()

    def closeEvent(self, QCloseEvent):
        self.close()
        self.parent().show()
