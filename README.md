# **Teensy Magnetometer** #

This README covers the installation and use of the lab-built software for the teensy-based magnetometer.


### **What can the device/software do?** ###

* Visualize the 3 spatial components (bx, by, bz) of the magnetic field near the sensor in real time
* Record sensor data to a .csv


### **How do I get set up?** ###

This software works on both linux and windows operating systems. The following instructions work for both operating systems.

1. Make a new directory and clone the repository there
2. Make a virtual environment with `python 3.8` in this directory and install the required dependencies by running `pip install -r requirements.txt` in the terminal
3. Run `pip list` and verify that the packages and versions match those listed in `requirements.txt`

### **Never done this kind of thing before?** ###

There are many package and environment managers for Python and beyond. If you have no preference, `conda` is a good place to start.

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. Make a new directory and clone the repository there
3. Open an Anaconda Prompt and `cd` to the directory that you just created
4. Make a virtual environment with the appropriate dependencies by running `conda env create -f environment.yml`
5. Activate the virtual environment by running `conda activate .venv-magnetometer`
6. Run `conda list` and verify that the packages and versions match those listed in requirements.txt

### **How do I use it?** ###

#### ** Start the GUI: ** ####
1. Plug the teensy-based magnetometer into one of the USB ports on your machine. After a few seconds the OLED display on the device will light up.
2. Ensure your virtual environment is active
3. Run `python magnetometer.py` in the terminal/Anaconda Prompt. The GUI will open and display the field recordings in real-time.


#### ** Recording Data: ** ####
1. Enter the desired file name into the filename text box. Note that the string '.csv' will be automatically appended to whatever you enter, so don't add it.
2. When ready to record, press "Start Recording"
3. When ready to stop recording, press "Stop Recording". A .csv file with your specified name will be written in the working directory.


#### ** Changing Axis Limits: ** ####
Sometimes it can be useful to change the axis limits to get a better look at the field in real time. To do this, enter the desired axis limits (ensure that lower limit < upper limit) into the text boxes and press the corresponding button. 


#### ** When Finished ** ####
Important! You must press the "Close Window" button in the GUI window to close and end the program.

This is because `Tcl` is slow to update in `tkinter` GUI's. If you neglected to use the "Close Window" button, the program may still be running in the terminal. Run "ctrl + c" as many times as it takes to kill the program. On WSL this may not even be enough and you may need to kill the terminal.


### **Who do I talk to if I have issues?** ###

This software was written by Travis Allen in June 2022