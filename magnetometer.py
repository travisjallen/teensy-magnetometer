"""

Software for Telerobotics Lab custom magnetometer.
Allows for real-time visualization of a 3D magnetic 
field, as well as the ability to record data to a 
.csv file. Tested on Ubuntu 20.04. 

Required OTS libraries that must be installed in your
virtual environment:
serial, matplotlib, numpy (installed with matplotlib)

Required custom libraries: teensytk, teensyserial

Author: Travis Allen
05.22

"""

##-----------Imports--------------

## GUI
# import teensytk
import teensytk

## serial
import teensyserial

##-----------End Imports-----------

def main():
    ## set a baud rate
    baudRate = 9600

    ## Initialize the teensy
    teensy = teensyserial.open(baudRate)

    ## run the GUI
    # teensytk.tkmain(teensy)
    teensytk.tkmain(teensy)


if __name__ == '__main__':
    main()