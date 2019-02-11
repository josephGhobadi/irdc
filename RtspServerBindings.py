import os
import platform
import psutil
import subprocess
import time


class rtspServer:
    def __init__(self):
        self.rtspServer_command = ""

        self.platform = platform.system()
        self.current_file_address = os.path.dirname(os.path.abspath(__file__))

        ''' make commands '''
        self.make_rtspServer_command()

        ''' rtspServer process '''
        self.process = None
        self.run_rtspServer()

    def make_rtspServer_command(self):
        if self.platform == "Linux":
            self.rtspServer_command = self.current_file_address + "/bin/unix/rtspServer"
        elif self.platform == "Windows":
            self.rtspServer_command = self.current_file_address + "\\bin\\windows\\rtspServer.exe"

    def check_alive(self):
        try:
            os.kill(self.process.pid, 0)
            return True
        except OSError:
            return False

    def run_rtspServer(self):
        self.process = subprocess.Popen(self.rtspServer_command, shell=True,
                                        stdin=None, stdout=None, stderr=None, close_fds=True)
        print(self.rtspServer_command)

    def __del__(self):
        for proc in psutil.process_iter():
            # check whether the process name matches
            if "rtspServer" in proc.name():
                proc.kill()
