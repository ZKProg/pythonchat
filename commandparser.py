import os 
import sys
import re

class CommandParser:

    def __init__(self):
        pass

    def parseCommand(self, unparsedData):
        """
        Parse the command, and get the associated data
        """
        pattern = '^#(?P<commandType>(.*)):(?P<commandData>(.*))#$'
        result = re.search(pattern, unparsedData)
        if result != None:
            commandType = result['commandType']
            commandData = result['commandData']
            return (commandType, commandData)  
        else:
            return (None, None)  