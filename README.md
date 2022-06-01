# **Teensy Magnetometer** #

This README covers the installation and use of the lab-built software for the teensy-based magnetometer.


### **What can the device/software do?** ###

* Visualize the 3 spatial components (bx, by, bz) of the magnetic field near the sensor in real time
* Record sensor data to a .csv


### **How do I get set up?** ###

This software works on both linux and windows operating systems. The following instructions work for both operating systems, but differ slightly depending on whether you use `pip` or `conda`.


#### ** `pip` setup instructions: ** ####
1. Make a new directory and clone the repository there
2. Open a terminal and `cd` to the directory that you just created
3. Make a virtual environment called "_mag" by running `virtualenv -p /usr/bin/python3.8 _mag` in the terminal
4. Activate the virtual environment by running `source _mag/bin/activate` in the terminal
5. Install the required dependencies by running `pip install -r requirements.txt` in the terminal
6. Run `pip list` and verify that the packages and versions match those listed in `requirements.txt`


#### ** `conda` setup instructions: ** ####
1. Make a new directory and clone the repository there
2. Open a terminal and `cd` to the directory that you just created
3. Make a virtual environment called "_mag" by running `conda create --name _mag python==3.8` in the terminal
4. Activate the virtual environment by running `conda activate _mag` in the terminal
5. Install the required dependencies by running `conda install --file requirements.txt` in the terminal
6. Run `conda list` and verify that the packages and versions match those listed in `requirements.txt`


### **How do I use it?** ###

#### ** Start the GUI: ** ####
1. Plug the teensy-based magnetometer into one of the USB ports on your machine. After a few seconds the OLED display on the device will light up.
2. Ensure your virtual environment is active (see step 4 in either the `pip` or `conda` instructions)
3. Run `python magnetometer.py` in the terminal. The GUI will open and display the field recordings in real-time.


#### ** Recording Data: ** ####
1. Enter the desired file name into the filename text box. Note that the string '.csv' will be automatically appended to whatever you enter, so there is no need to add it.
2. When ready to record, press "Start Recording"
3. When ready to stop recording, press "Stop Recording". A .csv file with your specified name will be written in the working directory.


#### ** Changing Axis Limits: ** ####
Sometimes it can be useful to change the axis limits to get a better look at the field in real time. To do this, enter the desired axis limits (ensure that lower limit < upper limit) into the text boxes and press the corresponding button. 

#### ** When Finished ** ####
1. Press "ctrl + c" in the GUI window. On windows this will close the GUI and kill the prcess in the terminal.
2. If the process is still running in the terminal (i.e. the GUI window is open but not updating), run "ctrl + c" in the terminal. You may have to do this up to three times.
3. If the process is still running, close the terminal. `Tcl` is slow to update in `tkinter` GUI's, so sometimes this happens. Work on a fix to this is ongoing.


### **Who do I talk to if I have issues?** ###

This software was written by Travis Allen in June 2022