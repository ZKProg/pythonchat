import os
import sys
import threading
import socket as s 
import sqlite3 as sql
from queue import Queue

############################################################################
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
        self.getInputThread = threading.Thread(target=self.getInput)
        self.recvThread = threading.Thread(target=self.recv)

    def connect(self):
        """
        Connects to the server.
        """
        print(f'Attempting connection to {self.ADDR}:{self.PORT}')
        try:
            self.socket.connect((self.ADDR, self.PORT))
            self.isLive = True
            self.getInputThread.start()
            self.recvThread.start()
            
        except OSError as e:
            print('Error creating the connection: {}'.format(e))
            sys.exit(-1)

    #######################################################################
    # Threaded methods

    def getInput(self):
        while self.isLive:
            command = input('> ')
            dataToSend = bytes(command, 'utf-8')
            try:
                self.socket.send(dataToSend)
            except ConnectionResetError as e:
                pass
            except BrokenPipeError as e:
                pass
            except OSError as e:
                self.isLive = False

    def sendData(self, dataString):
        data = bytes(dataString, 'utf-8')
        try:
            self.socket.send(data)
        except BrokenPipeError as e:
            self.closeClient(e)
        except ConnectionResetError as e:
            self.closeClient(e)
        except OSError as e:
            self.closeClient(e)

    def recv(self):
        while self.isLive:
            try:
                data = self.socket.recv(1024)
            except BrokenPipeError as e:
                self.closeClient(e)
            except ConnectionResetError as e:
                self.closeClient(e)
            except OSError as e:
                self.closeClient(e)
            if not data: break
            if data.decode('utf-8') == 'closing':
                self.socket.close()              
                print('Closing connection command received.')  

            #print('From server: {}'.format(data.decode('utf-8')))

    def closeClient(self, e):
        print('Closing client: ', e)
        print('**** Press Enter to exit the client. ****')
        self.isLive = False
        




############################################################################
# Execute

if __name__ == '__main__':
    if os.name == 'nt': hostOs = 'Windows'
    print('Executing client on {} platform.'.format(hostOs))
    ADDR = '127.0.0.1'
    PORT = int(sys.argv[1])
    client = Client(addr=ADDR, port=PORT)
    client.connect()

