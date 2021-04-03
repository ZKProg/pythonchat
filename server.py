import os
import sys
import threading
import socket as s 
import sqlite3 as sql
import time
import re
from queue import Queue

################################################
# Connection
class Connection:

    def __init__(self, conn, addr, *args, **kwargs):
        self.conn = conn
        self.addr = addr
        self.isLive = True
        self.conn.send(b'Connection accepted by server.')
        self.receiveThread = threading.Thread(target=self.recv)
        self.receiveThread.start()

    def recv(self):
        while self.isLive:
            try:
                data = self.conn.recv(1024)
                data = data.decode('utf-8')
                commandType, commandData = self.parseCommand(data)
                self.executeCommand(commandType, commandData)
            except BrokenPipeError as e:
                self.isLive = False
                self.conn.close()
                print('Connection closed.')
                sys.exit(0)
            except ConnectionResetError as e:
                print(e)

    def parseCommand(self, unparseData):
        """
        Parse the command, and get the associated data
        """
        pattern = '^#(?P<commandType>(.*)):(?P<commandData>(.*))#$'
        result = re.search(pattern, unparseData)
        if result != None:
            commandType = result['commandType']
            commandData = result['commandData']
            return (commandType, commandData)  
        else:
            return (None, None)  
    

    def executeCommand(self, commandType, commandData):
        if commandType == 'quit':
            self.conn.send(b'closing')
            self.conn.close()
            self.isLive = False


################################################
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


if __name__ == '__main__':
    PORT = int(sys.argv[1])
    server = Server(port=PORT)
    server.launch()