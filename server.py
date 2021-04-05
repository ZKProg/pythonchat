import os
import sys
import threading
import socket as s 
import sqlite3 as sql
import time
import re
from queue import Queue
from connection import Connection

########################################################################################
# Server

class Server:

    def __init__(self, *args, **kwargs):
        self.connections = []
        self.isLive = False
        self.ADDR = ''
        self.PORT = 65000
        self.MAXLISTEN = 5
        if 'port' in kwargs:
            self.PORT = int(kwargs['port'])

    def launch(self):
        try:
            self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
            self.socket.bind(('', self.PORT))
            self.socket.listen(self.MAXLISTEN)
            self.acceptNewConnection()
        except OSError as e:
            print('Error creating the server: {}'.format(e))
            sys.exit(-1)

    def acceptNewConnection(self):
        try:
            conn, addr = self.socket.accept()
            connection = Connection(conn, addr)
            self.connections.append(connection)
            print('-' * 40)
            print('New connection from {}'.format(addr))
            print('Server running {} connection(s).'.format(len(self.connections)))
            print('-' * 40)
            self.acceptNewConnection()
        except OSError as e:
            print('Error accepting new connection: {}'.format(e))

##########################################################################################
# Execute

if __name__ == '__main__':
    PORT = int(sys.argv[1])
    server = Server(port=PORT)
    server.launch()