from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ScreenGrabber:
    def __init__(self):
        self.last_frame = False
        self.current_frame_diff_last_frame = False
        self._array = QByteArray()
        self._buffer = QBuffer(self._array)

    def grab(self):
        current_frame = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId())

        '''if sum(current_frame) == sum(self.last_frame):
            return 'same frames'''
        if not self.last_frame:
            self.last_frame = current_frame

        current_frame.save(self._buffer, 'jpeg')
        r = self._buffer.data()
        self._array.clear()
        self._buffer.close()
        return r
