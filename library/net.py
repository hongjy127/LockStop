import socket
import struct
from _thread import *

def server(ip, port, thread):
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        try:
            s.bind((ip, port))
            s.listen(1)
            while True:
                client_sockcet, addr = s.accept()
                start_new_thread(thread, (client_sockcet, addr))
        except Exception as e:
            print(e)

def send(writer ,data, save=0):
    writer.write(struct.pack('<L', len(data)))
    writer.write(struct.pack('<L', save))
    writer.write(data)
    writer.flush()

def receive(reader):
    data = reader.read(struct.calcsize('<L'))
    save = reader.read(struct.calcsize('<L'))
    data_len = struct.unpack('<L', data)[0]

    if not data_len:
        return (None, 0)
    data = reader.read(data_len)

    return (data, data_len, save)
    

        