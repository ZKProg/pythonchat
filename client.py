import os
import sys
import threading
import socket as s 
import sqlite3 as sql
from queue import Queue

##########################################
# Client

class Client:
    """
    Simple network client
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor. Initializes the socket and get the arguments
        if they are present.
        """
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.isLive = False
        self.ADDR = '127.0.0.1'
        self.PORT = 65000

        if 'addr' in kwargs:
            self.ADDR = kwargs['addr']
        if 'port' in kwargs:
            self.PORT = int(kwargs['port'])
        # Threading -----------------------------------------------
        self.sendThread = threading.Thread(target=self.send)
        self.recvThread = threading.Thread(target=self.recv)

    def connect(self):
        """
        Connects to the server.
        """
        print(f'Attempting connection to {self.ADDR}:{self.PORT}')
        try:
            self.socket.connect((self.ADDR, self.PORT))
            self.isLive = True
            self.sendThread.start()
            self.recvThread.start()
            
        except OSError as e:
            print('Error creating the connection: {}'.format(e))
            sys.exit(-1)

    def send(self):
        while self.isLive:
            command = input('> ')
            dataToSend = bytes(command, 'utf-8')
            self.socket.send(dataToSend)

    def recv(self):
        while self.isLive:
            data = self.socket.recv(1024)
            if not data: break
            if data.decode('utf-8') == 'closing':
                print('Closing connection command received')
                self.socket.close()
                self.isLive = False
            print('From server: {}'.format(data.decode('utf-8')))


if __name__ == '__main__':
    ADDR = '127.0.0.1'
    PORT = int(sys.argv[1])
    client = Client(addr=ADDR, port=PORT)
    client.connect()

