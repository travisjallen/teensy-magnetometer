# **Teensy Magnetometer** #

This README covers the installation and use of the lab-built software for the teensy-based magnetometer.

---

### **What can the device/software do?** ###

* Visualize the 3 spatial components (bx, by, bz) of the magnetic field near the sensor in real time
* Record sensor data to a .csv

---

### **How do I get set up?** ###

This software works on linux, windows, and windows subsystem for linux (WSL) operating systems. The setup procedures are similar, but one extra step is required to get setup on a linux machine. This step is **not** required for WSL. Here's how to get started:

1. Make a new directory and clone the repository there
2. **If using linux (not WSL):** `cd` to the directory in which the repository is located and run `./install_teensy_udev_rule.sh`. This requires root privileges. This step allows serial commuincation between your compter and the teensy.
3. Make a virtual environment with `python 3.8` in this directory and install the required dependencies by running `pip install -r requirements.txt` in the terminal
4. Run `pip list` and verify that the packages and versions match those listed in `requirements.txt`

---

### **Never done this kind of thing before?** ###

There are many package and environment managers for Python and beyond. If you have no preference, `conda` is a good place to start.

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
2. Make a new directory and clone the repository there
3. Open an Anaconda Prompt and `cd` to the directory that you just created
4. Make a virtual environment with the appropriate dependencies by running `conda env create -f environment.yml`
5. Activate the virtual environment by running `conda activate .venv-magnetometer`
6. Run `conda list` and verify that the packages and versions match those listed in requirements.txt

---

### **How do I use it?** ###

**Start the GUI:**
1. Plug the teensy-based magnetometer into one of the USB ports on your machine. After a few seconds the OLED display on the device will light up.
2. Ensure your virtual environment is active
3. Run `python magnetometer.py` in the terminal/Anaconda Prompt. The GUI will open and display the field recordings in real-time.


**Recording Data:**
1. Enter the desired file name into the filename text box. Note that the string '.csv' will be automatically appended to whatever you enter, so don't add it.
2. When ready to record, press "Start Recording"
3. When ready to stop recording, press "Stop Recording". A .csv file with your specified name will be written in the working directory.


**Changing Axis Limits:**

Sometimes it can be useful to change the axis limits to get a better look at the field in real time. To do this, enter the desired axis limits (ensure that lower limit < upper limit) into the text boxes and press the corresponding button. 


**When Finished:**

Important! You must press the "Close Window" button in the GUI window to close and end the program.

This is because `Tcl` is slow to update in `tkinter` GUI's. If you neglected to use the "Close Window" button, the program may still be running in the terminal. Run "ctrl + c" as many times as it takes to kill the program. On WSL this may not even be enough and you may need to kill the terminal. A fix to this issue is being investigated. 

---

### **What's in this repository?**
- `magnetometer.py` is the main script. This is the only thing you will run when you use the sensor. 
- `teensyserial.py` is a module which establishes and supports serial communication with the teensy. It is called by `magnetometer.py`.
- `teensytk.py` is a module which establishes and supports the GUI. It is called by `magnetometer.py`.
- `environment.yml` is a YAML file which allows for a user to easily set up a `conda` environment with the necessary dependencies.
- `requirements.txt` is a list of dependencies that are required for this program to run.
- `00-teensy.rules` are the udev rules which are required to enable serial communication between linux machines and the teensy.
- `install_teensy_udev_rule.sh` is a bash script that installs the udev rules which are required to enable serial communication between linux machines and the teensy.
- `extras` is a folder which contains ancillary and legacy code and documentation. You will not need anything in this folder unless you seek to fundamentally alter the way this device operates. The code that is on the teensy can be found here. The original creator of this device set it up such that it could be used with ROS. Some documentation and code regarding use with ROS can be found here. The sensor on the magnetometer is an Infineon TLV493D, and its documentation can be found here. To reiterate: you probably don't need anything in here.
- `README.md` is this file.

---

### **Who do I talk to if I have issues?** ###

This software was written by Travis Allen in June 2022
