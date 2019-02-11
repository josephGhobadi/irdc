from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ConnectToRemote import ConnectToRemote
from ShareThisDesktop import ShareThisDesktop
import re


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.share = None
        self.share_thread = ShareThisDesktop()
        check_share_code_regex = r"^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])" \
                                 r":([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"
        self.pattern = re.compile(check_share_code_regex)
        self.remote_command = None
        self.connect_to_remote_object = None

        self.sizeHint = lambda: QSize(250, 100)
        self.move(100, 50)
        wid = QWidget(self)
        self.setCentralWidget(wid)
        layout = QVBoxLayout()

        _1stHLayout = QHBoxLayout()
        self.destination_id = QLineEdit()
        _1stHLayout.addWidget(self.destination_id)
        connect_to_remote = QPushButton('Connect')
        _1stHLayout.addWidget(connect_to_remote)
        connect_to_remote.clicked.connect(self.connect_to_remote_machine)
        layout.addLayout(_1stHLayout)

        _2ndHLayout = QHBoxLayout()
        self.share_for_remote_btn = QPushButton('Share Your Desktop')
        _2ndHLayout.addWidget(self.share_for_remote_btn)
        self.share_for_remote_btn.clicked.connect(self.share_this_desktop)
        layout.addLayout(_2ndHLayout)

        wid.setLayout(layout)
        self.show()

    def connect_to_remote_machine(self):
        remote_id = self.destination_id.text()
        if self.pattern.match(remote_id):
            self.hide()
            self.connect_to_remote_object = ConnectToRemote(self, remote_id)
        else:
            alert = QMessageBox()
            alert.setText("Wrong share code !\nYou should insert something like 1234:1234")
            alert.exec_()

    def share_this_desktop(self):
        self.share_for_remote_btn.setText('Trying to share...')
        self.share_thread.start()
        self.share = ShareThisDesktop()
        self.share.lunch()
        if self.share.status:
            self.share_for_remote_btn.setText(self.share.shareCode + ' stop sharing!')
        elif self.share.fail:
            alert = QMessageBox()
            alert.setText("Connection Failed")
            alert.exec_()
