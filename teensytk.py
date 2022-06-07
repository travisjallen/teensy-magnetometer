"""
Teensy Tk

Builds and maintains GUI

Author: Travis Allen
05.22
"""

#------------ Imports --------------------
import tkinter as tk
import time

## matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import numpy as np

#------------ End Imports ----------------

def tkmain(teensy):
    """
    establishes and runs the GUI
    """
    root = tk.Tk()
    gui = Window(teensy, root)
    root.geometry('1037x500')
    # root.bind('<Control-c>', root.quit)
    tk.mainloop()
    

class StylizedButton(tk.Button):
    def __init__(self, *args, **kwargs):
        '''
        makes the "Close Window" button more noticeable
        '''
        f = tk.Frame(args[0]
                  ,highlightbackground="black"
                  ,highlightcolor="black"
                  ,highlightthickness=1)
        super().__init__(f, *args[1:], **kwargs)
        self.configure( activebackground='#808080'
                       ,activeforeground='black'
                       ,background='#a6a6a6'
                       ,foreground='black'
                       ,relief='solid')
        f.pack()


class Window(tk.Frame):
    def __init__(self, teensy, master = None):
        ## matplotlib initialization
        self.y_lower_limit = -20
        self.y_upper_limit = 20
        self.lag = 70
        
        ## csv write initialization
        self.start_time = 0.0
        self.filename = ''
        self.recording = False
        self.csv_data = np.zeros((1,4))
        
        ## tkinter initialization
        tk.Frame.__init__(self,master)
        self.master = master
        self.init_window(teensy)
        
    
    ## make a frame for the data capture section
    def init_data_frame(self):
        """
        makes a frame for the data capture region of the root, then populates it and returns the frame
        """
        data_frame = tk.Frame(self,width = 400, height = 200)

        ## label
        tk.Label(data_frame, text = "Enter Filename. \".csv\" automatically appended").pack(fill = 'x', expand = True)# grid(row = 0, column = 1)

        ## entry
        self.filename_entry = tk.Entry(data_frame, width = 15)
        self.filename_entry.insert(0,'filename...')
        self.filename_entry.bind('<FocusIn>', self.on_entry_click_filename)
        self.filename_entry.bind('<FocusOut>', self.on_focusout_filename)
        self.filename_entry.config(fg = 'grey')
        self.filename_entry.pack(fill = 'x', expand = True)
        
        ## button
        self.enter_button = tk.Button(data_frame, text = "Enter", padx = 150, command = self.filename_enter_button_func)
        self.enter_button.pack(fill = 'x', expand = True)

        return data_frame


    ## make a frame for the recording section
    def init_recording_frame(self):
        """
        makes a frame for the recording section of the root, then populates it and returns the frame
        """
        recording_frame = tk.Frame(self, width = 400, height = 100)

        ## label
        tk.Label(recording_frame, text = "Recording:").grid(row = 0, column = 0,columnspan = 2)
        
        ## "start recording" button
        self.start_record_button = tk.Button(recording_frame, 
                                            text = "Start Recording",
                                            padx = 20,
                                            command = self.start_button_func)
        self.start_record_button.grid(row = 1, column = 0, columnspan = 1)

        ## "stop recording" button
        self.stop_record_button = tk.Button(recording_frame,
                                            text = "Stop Recording",
                                            padx = 20,
                                            command = self.stop_button_func)
        self.stop_record_button.grid(row = 1, column = 1, columnspan = 1)

        return recording_frame

    
    def init_axes_frame(self):
        """
        makes a frame for the axes change and quit section of the root, then populates it and returns the frame
        """
        axes_frame = tk.Frame(self, width = 400, height = 300)
        
        ## label
        tk.Label(axes_frame, text = "Set Y-Axis Limits").grid(row = 0, column = 0, columnspan = 2)

        ## lower entry
        self.set_y_lower_entry = tk.Entry(axes_frame, width = 21)
        self.set_y_lower_entry.insert(0,f"{self.y_lower_limit}")
        self.set_y_lower_entry.bind('<FocusIn>', self.on_entry_click_y_lower)
        self.set_y_lower_entry.bind('<FocusOut>', self.on_focusout_y_lower)
        self.set_y_lower_entry.config(fg = 'grey')
        self.set_y_lower_entry.grid(row = 1, column = 0, columnspan = 1)
        
        ## lower button
        self.set_y_lower_button = tk.Button(axes_frame, text = "Set Lower Y-Axis Limit", command = self.set_y_lower_button_func)
        self.set_y_lower_button.grid(row = 2, column = 0, columnspan = 1)
        
        ## upper entry
        self.set_y_upper_entry = tk.Entry(axes_frame, width = 21)
        self.set_y_upper_entry.insert(0,f"{self.y_upper_limit}")
        self.set_y_upper_entry.bind('<FocusIn>', self.on_entry_click_y_upper)
        self.set_y_upper_entry.bind('<FocusOut>', self.on_focusout_y_upper)
        self.set_y_upper_entry.config(fg = 'grey')
        self.set_y_upper_entry.grid(row = 1, column = 1, columnspan = 1)
        
        ## upper button
        self.set_y_upper_button = tk.Button(axes_frame, text = "Set Upper Y-Axis Limit", command = self.set_y_upper_button_func)
        self.set_y_upper_button.grid(row = 2, column = 1, columnspan = 1)

        return axes_frame

    def init_close_frame(self):
        """
        makes a frame for "Close Window" button. when called, 
        "Close Window" destroys root and calls exit()
        """
        close_frame = tk.Frame(self, width = 400, height = 200)
        self.close_window_button = StylizedButton(close_frame, text = "Close Window", padx = 40, pady  = 20, command = self.quit)
        self.close_window_button.grid(row = 0, column = 0, columnspan = 2)

        return close_frame

    
    def init_window(self,teensy):
        """
        sets up the main window and the matplotlib animation
        """
        ## set up tkinter basic stuff
        graph_row_span = 4
        self.master.title("Telerobotics Magnetometer")
        self.grid(row = 0, column = 0,rowspan = graph_row_span)
        

        ## set up matplotlib stuff
        self.fig = plt.figure(figsize=(7,5), dpi = 100)
        self.axes = self.fig.add_subplot(1,1,1)
        plt.title("Instantaneous Field")
        plt.ylabel("Field Strength [mT]")

        
        ## set up the constituent frames
        data_frame = self.init_data_frame()
        data_frame.grid(row = 0, column = 1, columnspan = 1)

        recording_frame = self.init_recording_frame()
        recording_frame.grid(row = 1, column = 1, columnspan = 1)

        axes_frame = self.init_axes_frame()
        axes_frame.grid(row = 2, column = 1, columnspan = 1)

        close_frame = self.init_close_frame()
        close_frame.grid(row = 3, column = 1, columnspan = 1)


        def animate(ii):
            """
            animation function for matplotlib. serial reads data, records data for csv, animates data
            """
            data = teensy.read()
            self.csv_arrange(data)

            ## organize the data            
            x.append(ii)
            bx.append(data[0,0])
            by.append(data[1,0])
            bz.append(data[2,0])
            
            ## plot it
            bxLine.set_data(x,bx)
            byLine.set_data(x,by)
            bzLine.set_data(x,bz)
            
            ## set moving axes
            plt.xlim(ii-self.lag,ii+6)

        ## determine the number of incoming symbols per serial readline and set the animation interval
        refresh = int(1000/(teensy.baudRate/float(teensy.numSym())))

        ## Empty lists for data
        x,bx,by,bz = [], [], [], []

        ## initialize the line objects
        bxLine, = self.axes.plot([], [], color="blue", label = 'bx')
        bxLine.set_data([], [])
        byLine, = self.axes.plot([], [], color="red", label = 'by')
        byLine.set_data([], [])
        bzLine, = self.axes.plot([], [], color="green", label = 'bz')
        bzLine.set_data([], [])

        ## matplotlib figure setup
        style.use("ggplot")
        self.axes.set_ylim(self.y_lower_limit,self.y_upper_limit)
        plt.grid(linestyle = '--', linewidth = 0.5)
        self.axes.yaxis.set_label_position("right")
        self.axes.yaxis.tick_right()
        self.axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox = True, shadow = True, ncol = 3)

        ## tkinter/matplotlib integration
        self.canvas = FigureCanvasTkAgg(self.fig, master = self)
        self.canvas.get_tk_widget().grid(row = 0, column = 0, rowspan = graph_row_span)

        ## run the animation and show it        
        self.ani = animation.FuncAnimation(self.fig, animate, interval = refresh , blit = False)


    ## csv arrange method
    def csv_arrange(self,data):
        """
        arranges sensor data into numpy array (if recording is True)
        """
        if self.recording:
            timestamp = time.perf_counter() - self.start_time
            next_line = np.array([[data[0, 0], data[1, 0], data[2, 0], timestamp]])
            self.csv_data = np.append(self.csv_data, next_line, axis = 0)
            

    def csv_write(self):
        """
        writes stored sensor data to .csv file with user-specified filename.
        doesn't allow user to record data with default or no filename
        """
        if self.recording:
            if self.filename == '' or self.filename == "filename...":
                print("Error! No filename entered. Data not recorded.")
                self.recording = False
            else:
                np.savetxt(self.filename,self.csv_data,delimiter = ',')
        
        ## cleans up after itself
        self.recording = False


    ## ======================================================/
    ## button methods
    ## ======================================================/
    def quit(self):
        """
        quits program to circumvent slow Tcl reaction/update
        """
        self.master.destroy()
        exit()
        


    ## filename enter button method
    def filename_enter_button_func(self):
        ## get the filename from the entry and add ".csv" to the end
        tempname = self.filename_entry.get()
        self.filename = f"{tempname}.csv"


    ## start recording button
    def start_button_func(self):
        ## if 'start recording' is clicked, set self.recording to True and set the start time
        self.recording = True
        self.start_time = time.perf_counter()


    ## stop recording button
    def stop_button_func(self):
        ## if 'stop recording' is clicked, call csv_write, which sets self.recording to false
        self.csv_write()
        self.recording = False

    
    ## set y axis lower button method
    def set_y_lower_button_func(self):
        ## check to see if the entry is nonempty 
        if self.set_y_lower_entry.get() != '':
            ## reset the axis limits
            self.y_lower_limit = float(self.set_y_lower_entry.get())
            self.axes.set_ylim(self.y_lower_limit,self.y_upper_limit)
        

    ## set y axis upper button method
    def set_y_upper_button_func(self):
        ## check to see if the entry is nonempty 
        if self.set_y_upper_entry.get() != '':
            ## reset the axis limits
            self.y_upper_limit = float(self.set_y_upper_entry.get())
            self.axes.set_ylim(self.y_lower_limit,self.y_upper_limit)


    ## on entry click method for filename text entry
    def on_entry_click_filename(self, event):
        if self.filename_entry.get() == 'filename...':
            self.filename_entry.delete(0,"end")
            self.filename_entry.insert(0,'')
            self.filename_entry.config(fg = 'black')
            
    
    ## on entry click method for y axis lower text entry
    def on_entry_click_y_lower(self, event):
        if self.set_y_lower_entry.get() == self.y_lower_limit:
            self.set_y_lower_entry.delete(0,"end")
            self.set_y_lower_entry.insert(0,'')
            self.set_y_lower_entry.config(fg = 'black')
    
    
    ## on entry click method for y axis upper text entry
    def on_entry_click_y_upper(self, event):
        if self.set_y_upper_entry.get() == 'y-axis upper limit':
            self.set_y_upper_entry.delete(0,"end")
            self.set_y_upper_entry.insert(0,'')
            self.set_y_upper_entry.config(fg = 'black')
    
    
    ## on focus out method for filename text entry
    def on_focusout_filename(self, event):
        if self.filename_entry.get() == '':
            self.filename_entry.insert(0,'filename...')
            self.filename_entry.config(fg = 'grey')

    
    ## on focus out method for y axis lower text entry
    def on_focusout_y_lower(self, event):
        if self.set_y_lower_entry.get() == '':
            self.set_y_lower_entry.insert(0,'y-axis lower limit')
            self.set_y_lower_entry.config(fg = 'grey')


    ## on focus out method for y axis upper text entry
    def on_focusout_y_upper(self, event):
        if self.set_y_upper_entry.get() == '':
            self.set_y_upper_entry.insert(0,'y-axis upper limit')
            self.set_y_upper_entry.config(fg = 'grey')

    
    