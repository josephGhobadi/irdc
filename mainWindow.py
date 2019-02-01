from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ConnectToRemote import ConnectToRemote
from ShareThisDesktop import ShareThisDesktop


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
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
        if remote_id != "":
            ConnectToRemote(remote_id)
            ''' TO DO ! '''

    def share_this_desktop(self):
        self.share_for_remote_btn.setText('Trying to share...')
        share_status = ShareThisDesktop()
        if share_status.isConnected:
            self.share_for_remote_btn.setText(share_status.shareCode + ' stop sharing!')
        else:
            alert = QMessageBox()
            alert.setText("Connection Failed")
            alert.exec_()


