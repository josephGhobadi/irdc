import threading
import subprocess
import platform
import os
import signal
import screeninfo
from time import sleep


class ShareThisDesktop:
    def __init__(self):
        self.isConnected = False
        self.shareCode = 'NaN!'
        self.rtsp_process_id = 0
        self.ffmpeg_process_id = 0
        self.is_rtsp_server_started = False
        self.is_already_killing_server = False

        self.ffmpeg_command = ""
        self.rtsp_command = ""

        self.platform = platform.system()
        self.current_file_address = os.path.dirname(os.path.abspath(__file__))

        ''' make commands '''
        self.make_ffmpeg_command()
        self.make_rtsp_command()

    def make_ffmpeg_command(self):
        ffmpeg_arguments = ""
        if self.platform == "Linux":
            ffmpeg_arguments = " -video_size "
            ffmpeg_arguments = ffmpeg_arguments + screeninfo.get_monitors()[0].width + "x"
            ffmpeg_arguments = ffmpeg_arguments + screeninfo.get_monitors()[0].height
            ffmpeg_arguments = ffmpeg_arguments + " -f x11grab -i :1 "
        elif self.platform == "Windows":
            ffmpeg_arguments = ffmpeg_arguments + " -f gdigrab "
        ffmpeg_arguments = ffmpeg_arguments + " -framerate 15 "
        ffmpeg_arguments = ffmpeg_arguments + " -rtsp_transport tcp -f rtsp rtsp://localhost:1554/test "

        if self.platform == "Linux":
            self.ffmpeg_command = self.current_file_address + "/bin/unix/ffmpeg" + ffmpeg_arguments
        elif self.platform == "Windows":
            self.ffmpeg_command = self.current_file_address + "\\bin\\windows\\ffmpeg.exe" + ffmpeg_arguments

    def make_rtsp_command(self):
        if self.platform == "Linux":
            self.rtsp_command = self.current_file_address + "/bin/unix/rtspServer"
        elif self.platform == "Windows":
            self.rtsp_command = self.current_file_address + "\\bin\\unix\\rtspServer"

    def kill_server(self):
        if self.is_already_killing_server:
            return

        self.is_already_killing_server = True
        ''' kill ssh port forwarding '''

        ''' kill ffmpeg and rtsp '''
        os.kill(self.rtsp_process_id, signal.SIGTERM)
        os.kill(self.ffmpeg_process_id, signal.SIGTERM)
        ''' kill command server '''

    def lunch_ffmpeg(self):
        while not self.is_rtsp_server_started:
            sleep(0.5)
        process = subprocess.Popen(self.ffmpeg_command)
        self.ffmpeg_process_id = process.pid
        process.wait()
        self.kill_server()
        return

    def lunch_rtsp_server(self):
        process = subprocess.Popen(self.rtsp_command)
        self.is_rtsp_server_started = True
        self.rtsp_process_id = process.pid
        process.wait()
        self.kill_server()
        return

    def lunch(self):
        ''' Run Command Server '''

        ''' Run Stream Server'''
        rtsp_thread = threading.Thread(target=self.lunch_rtsp_server)
        rtsp_thread.start()

        ffmpeg_thread = threading.Thread(target=self.lunch_ffmpeg)
        ffmpeg_thread.start()
        # returns immediately after the thread starts
        ''' Run ssh port forwarding '''
        self.isConnected = True
