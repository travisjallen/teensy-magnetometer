"""
teensyserial

Contains all relevant functionality for serial communication 
to Teensy-based Telerobotics Lab magnetometer

05.22
Author: Travis Allen
"""
##-----------Imports--------------

import serial
import sys
import numpy as np
import time

##-----------End Imports-----------

## version number
version_no = 1.0

class SerialPort:
    def __init__(self,port,baud_rate):
        ## set the port and baud rate
        self.port = serial.Serial(port,baud_rate)
        self.baudRate = baud_rate

        ## close the port first then open it
        self.port.close()
        self.port_open()
        
        ## initialize an np array of zeros for the field
        self.field = np.zeros((3,1))


    def port_open(self):
        """
        checks if port is closed, then opens it if not
        """
        if not self.port.isOpen():
            self.port.open()

    
    def parse(self,line):
        """
        uses known format of incoming serial data to split and assign the data to the field
        """
        ## change the line type from byte to string and split it by commas
        line = str(line)
        entries = line.split(',')

        ## assign b's [[bx], [by], [bz]]
        self.field[0,0] = float(entries[0][2:])
        self.field[1,0] = float(entries[1])
        self.field[2,0] = float(entries[2][0:-5])

    
    def read(self):
        """
        serial-reads teensy and returns magnetic field as a numpy array:
        [[bx], [by], [bz]]
        """
        data = self.port.readline()
        self.parse(data)
        return self.field


    def numSym(self):
        """
        determines the number of symbols in an incoming serial message
        """
        data = self.port.readline()
        return len(data)


def comcheck(baudRate):
    """
    checks user's OS and finds the com or dev/tty that the teensy is on
    """
    ## notify the user
    print("Searching for operating system...")
    p = sys.platform

    ## decide if windows or linux
    if p == 'linux':
        print("Linux operating system detected")
        base_str = '/dev/ttyS'
        
    elif p == 'win32':
        print("Windows operating system detected")
        base_str = 'COM'
    else:
        raise ValueError('User\'s Operating System Not Supported')

    ## set the number of com ports to loop through and check them
    print("Searching for Teensy...")
    ports = 16
    possibleCom = []
    for port in range(ports):
        ## see if we can open port
        try:
            serial_port = serial.Serial(f"{base_str}{port}",baudRate)
            serial_port.isOpen()
            
            ## if we can, append the port number to the list of possible ports and close the port
            possibleCom.append(port)
            serial_port.close()

        except IOError:
            pass

    ## loop through possibleCom and see which port has the appropriate data coming in
    for port in possibleCom:
        serial_port = serial.Serial(f"{base_str}{port}",baudRate,timeout = 2)
        serial_port.close()
        serial_port.open()

        ## read a line and compare it to the known format
        line = str(serial_port.readline())
        if line[0] == 'b' and line[-2:] == 'n\'':
            ## then this is the correct com port
            com = f"{base_str}{port}"
            print(f"Teensy is at {com}")
            return com
        else:
            raise Exception("\n\n\nTeensy not found! Make sure it is plugged in and the OLED is on...\n")

    

def open(baudRate):
    """
    Performs necessary actions upon opening the program:
    - finds the users OS
    - finds the serial port that the teensy is plugged into
    - opens the port that the teensy is plugged into
    """
    
    ## inform user that program has started
    print("******************************************************************************************************")
    print(f"\n\nUtah Telerobotics Lab Custom Magnetometer\nVersion {version_no}\n\n")
    print("******************************************************************************************************")

    ## find the serial port
    serialPort = comcheck(baudRate)
    
    ## open the serial port for the teensy and return the SerialPort object
    teensy = SerialPort(serialPort,baudRate)
    return teensy