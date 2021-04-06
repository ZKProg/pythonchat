import os
import sys
import threading
import socket as s 
import sqlite3 as sql
import time
import re
from queue import Queue
from commandparser import CommandParser

######################################################################################
# Connection

class Connection:

    def __init__(self, conn, addr, *args, **kwargs):
        self.conn = conn
        self.addr = addr
        self.isLive = True
        self.conn.send(b'Connection accepted by server.')
        self.receiveThread = threading.Thread(target=self.recv)
        self.receiveThread.start()
        self.commandParser = CommandParser()
        self.id = None
        self.isInitialized = False

    def recv(self):
        while self.isLive:
            try:
                data = self.conn.recv(1024)
                data = data.decode('utf-8')
                commandType, commandData = self.commandParser.parseCommand(data)
                self.executeCommand(commandType, commandData)
            except BrokenPipeError as e:
                self.isLive = False
                self.conn.close()
                print('Connection closed.')
                sys.exit(0)
            except ConnectionResetError as e:
                print(e)
    
    def executeCommand(self, commandType, commandData):
        if commandType == 'quit':
            self.sendData('closing')
            self.closeConnection()
        if commandType == 'init':
            self.id = commandData
            self.isInitialized = True
            print('Connection id initialize to: ', self.id)

    def sendData(self, dataString):
        data = bytes(dataString, 'utf-8')
        try:
            self.conn.send(data)
        except BrokenPipeError as e:
            self.isLive = False
            self.conn.close()
        except ConnectionResetError as e:
            pass

    def closeConnection(self):
        self.conn.close()
        self.isLive = False