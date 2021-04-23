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

def send(writer ,data, fname, save=0):
    writer.write(struct.pack('<L', len(data)))
    writer.write(struct.pack('<L', save))
    writer.write(struct.pack('<L', len(fname)))
    writer.write(data)
    writer.write(fname)
    writer.flush()

def receive(reader):
    data_len = reader.read(struct.calcsize('<L'))
    if not data_len: return None, None, None
    print('data len', data_len)
    data_len = struct.unpack('<L', data_len)[0]
    save = reader.read(struct.calcsize('<L'))
    save = struct.unpack('<L', save)[0]
    fname_len = reader.read(struct.calcsize('<L'))
    fname_len = struct.unpack('<L', fname_len)[0]
    print('fname len', fname_len)

    if not data_len:
        return (None, 0)
    data = reader.read(data_len)

    if not fname_len:
        return (None, 0)
    fname = reader.read(fname_len)

    return (data, data_len, fname, save)