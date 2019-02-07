import os
import random
import signal
import string
import subprocess
import multiprocessing
import time

file_name = "./" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) + ".tmp"


class RunSSH:
    def __init__(self, port):
        self.ssh_thread = None
        self.pipe = None
        self.stdout_result = ""
        self.stderr_result = ""
        self.out_thread = None
        self.err_thread = None
        self.success_string = b"Forwarding TCP connections from serveo.net"
        self.port = port

    def stdout_thread(self):
        x = b''
        while True:
            out = self.pipe.stdout.read(1)
            x = x + out
            if self.success_string in x:
                f = open(file_name, "w")
                f.write(x[x.find(b"serveo.net")+11:x.find(b"\n", x.find(b"serveo.net")+10)].decode("utf-8"))

            self.stdout_result = self.pipe.poll()
            if out == '' and self.stdout_result is not None:
                break

    def stderr_thread(self):
        while True:
            err = self.pipe.stderr.read(1)
            self.stderr_result = self.pipe.poll()
            if err == '' and self.stderr_result is not None:
                break

    def exec(self):
        self.pipe = subprocess.Popen(
            ['./bin/unix/ssh', '-o', 'StrictHostKeyChecking=no',
             '-F', '/dev/null', '-R', '0:localhost:'+self.port, 'serveo.net'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False
        )

        self.out_thread = multiprocessing.Process(name='stdout_thread', target=self.stdout_thread)
        self.err_thread = multiprocessing.Process(name='stderr_thread', target=self.stderr_thread)
        self.err_thread.daemon = True
        self.out_thread.daemon = True
        self.err_thread.start()
        self.out_thread.start()

    def __del__(self):
        os.kill(self.pipe.pid, signal.SIGTERM)
        if self.err_thread is not None:
            self.err_thread.terminate()

        if self.out_thread is not None:
            self.out_thread.terminate()


class ExposeNat:

    def __init__(self):
        self.host = "serveo.net"

    def run(self, port):
        is_connected = False
        ssh = None
        while not is_connected:
            retry_dial = 0
            while retry_dial < 5:
                print("hi")
                ssh = RunSSH(port)
                ssh.exec()
                time.sleep(5)
                if os.path.isfile(file_name):
                    is_connected = True
                    break
                del ssh

        f = open(file_name, "r")
        print(f.read())
        os.remove(file_name)
        return ssh
