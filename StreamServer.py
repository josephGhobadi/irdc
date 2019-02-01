import socket
import _thread
from ScreenGrabber import ScreenGrabber

''' 
    automata states:
    1: handshaking
    2: send Frame
    3: get Frame ack
'''


class StreamServer:
    def __init__(self):
        self.stream_bind = '127.0.0.1'
        self.stream_port = 5556
        self.buffer_size = 1024

    def server_handler(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.stream_bind, self.stream_port))
        s.listen(1)
        conn, address = s.accept()
        automata_state = 1
        buffer = b''
        grab_object = ScreenGrabber()
        while True:
            if automata_state == 1 or automata_state == 3:
                data = conn.recv(self.buffer_size)
                if not data:
                    conn.close()
                    print("closed")
                    break
                buffer = buffer + data

            if automata_state == 1:
                if b'{hello}!' in buffer:
                    buffer = b''
                    automata_state = 2

            elif automata_state == 2:
                im = grab_object.grab()
                if im == 'same frames':
                    conn.send(b'{same frames}!')
                else:
                    conn.send(im + b'{end of actions}!')
                    automata_state = 3

            elif automata_state == 3:
                if b'{frame ack}!' in buffer:
                    buffer = b''
                    automata_state = 1
                elif b'{connection close}' in buffer:
                    conn.close()
                    break
            print(buffer)

    def lunch_server(self):
        try:
            _thread.start_new_thread(self.server_handler, ())
        except:
            return False
        return True
