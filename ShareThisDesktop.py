from SshTunnel import ExposeNat
from FfmpegBinding import ffmpeg
from RtspServerBindings import rtspServer
from PyQt5.QtCore import QThread, pyqtSignal


class ShareThisDesktop(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.signal = pyqtSignal('PyQt_PyObject')

        self.status = False
        self.fail = False
        self.shareCode = 'NaN!'
        self.h = None
        self.s = None
        self._nat = None
        self._command = None

    def lunch(self):
        ''' Run Command Server '''

        ''' Run Stream Server'''
        self.h = rtspServer()
        self.s = ffmpeg(1554)
        ''' Run ssh port forwarding '''
        self._nat = ExposeNat()
        self._nat.run(1554)
        self._command = ExposeNat()
        self._command.run(1553)
        self.shareCode = str(self._nat.exposed_port) + ":" + str(self._command.exposed_port)
        self.status = True

    def __del__(self):
        ''' kill ssh port forwarding '''

        ''' kill ffmpeg and rtsp '''

        ''' kill command server '''
