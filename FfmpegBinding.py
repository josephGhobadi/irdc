import os
import platform
import subprocess
import screeninfo


class ffmpeg:
    def __init__(self, port):
        self.ffmpeg_command = ""

        self.platform = platform.system()
        self.current_file_address = os.path.dirname(os.path.abspath(__file__))

        ''' make commands '''
        self.make_ffmpeg_command(port)

        ''' ffmpeg process '''
        self.process = None
        self.run_ffmpeg()

    def make_ffmpeg_command(self, port):
        ffmpeg_arguments = " -hide_banner -loglevel panic"
        if self.platform == "Linux":
            ffmpeg_arguments = ffmpeg_arguments + " -video_size "
            ffmpeg_arguments = ffmpeg_arguments + str(screeninfo.get_monitors()[0].width) + "x"
            ffmpeg_arguments = ffmpeg_arguments + str(screeninfo.get_monitors()[0].height)
            ffmpeg_arguments = ffmpeg_arguments + " -f x11grab -i " + os.environ['DISPLAY'] + " "
        elif self.platform == "Windows":
            ffmpeg_arguments = ffmpeg_arguments + ffmpeg_arguments + " -f gdigrab "
        ffmpeg_arguments = ffmpeg_arguments + "-framerate 15"
        ffmpeg_arguments = ffmpeg_arguments + " -rtsp_transport tcp -f rtsp rtsp://localhost:" + str(port) + "/test"

        if self.platform == "Linux":
            self.ffmpeg_command = self.current_file_address + "/bin/unix/ffmpeg" + ffmpeg_arguments
        elif self.platform == "Windows":
            self.ffmpeg_command = self.current_file_address + "\\bin\\windows\\ffmpeg.exe" + ffmpeg_arguments

    def check_alive(self):
        try:
            os.kill(self.process.pid, 0)
            return True
        except OSError:
            return False

    def run_ffmpeg(self):
        self.process = subprocess.Popen(self.ffmpeg_command, shell=True,
                                        stdin=None, stdout=None, stderr=None, close_fds=True)

    def __del__(self):
        self.process.kill()
