import tkinter as tk
from time import sleep
from tkinter import messagebox
from PIL import Image, ImageTk

### ToDO
# - comment code
# - add another window class of type tk.Toplevel for the ToDo List window
# - add a function to create the ToDo List window in windowOne
# - add a function to create the ToDo List window in clockWindow

##Main window of Productivity App setup
class windowOne(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Productivity App")
        self.geometry("500x500")
        
        #Background image for WindowOne
        self.background_image = Image.open("C:/Users/Suzy/OneDrive/Documents/software dev 2/ProductivityApp_Final/Pink Wallpaper Girly.jpg")
        
        # Resizing image to match window size
        self.background_image = self.background_image.resize((500, 500))
        
        #Label to display background image for WindowOne
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self, image= self.background_photo)
        self.background_label.place(x= 0, y= 0)
        
        #Creating label widgets
        self.appTitle = tk.Label(self, text = "Productivity App")
        self.appTitle.place(x= 220, y= 50, anchor= tk.CENTER)
        self.toDoList = tk.Label(self)
        self.toDoList.place()
        self.timer_main = tk.Label(self)
        self.timer_main.place()
        
        #Button on Main window for TO DO LIST
        self.toDoList = tk.Button(self, text= "To Do List", command= None) # ToDo create a new ToDo window and function to call it
        self.toDoList.place(x= 220, y= 180, anchor= tk.CENTER)

        #Button on main window for TIMER
        self.timer_main = tk.Button(self, text= "Timer", command=self.createClockWindow)
        self.timer_main.place(x=220, y= 220, anchor= tk.CENTER )
        
    #Function to create Timer window
    def createClockWindow(self):
        my_clock_window: clockWindow = clockWindow(self)
        my_clock_window.grab_set() # force to the foreground
    
     
#Class for Timer window
class clockWindow(tk.Toplevel):
    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.title("Timer Countdown")
        self.geometry("500x500")
        
        #Background image for Timer
        self.background_image = Image.open("C:/Users/Suzy/OneDrive/Documents/software dev 2/ProductivityApp_Final/IMG_5141.JPG")
       
        # Resizing image to match window size
        self.background_image = self.background_image.resize((500, 500))
        
        #Label to display background image for Timer
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self, image= self.background_photo)
        self.background_label.place(x= 0, y= 0)
        
        #Creating label widgets
        self.timerTitle = tk.Label(self, text = "Timer")
        self.timerTitle.place(x= 220, y= 100, anchor= tk.CENTER)
        
        #Variables that show the time with default value
        self.hour = tk.StringVar(value="00")
        self.minute = tk.StringVar(value="00")
        self.second = tk.StringVar(value="00")

        #Take user input
        self.hourEntry = tk.Entry(self, width=3, textvariable=self.hour)
        self.hourEntry.place(x= 170, y= 180, anchor= tk.CENTER)

        self.minuteEntry = tk.Entry(self, width=3, textvariable=self.minute)
        self.minuteEntry.place(x= 220, y= 180, anchor= tk.CENTER)

        self.secondEntry = tk.Entry(self, width=3, textvariable=self.second)
        self.secondEntry.place(x= 270, y= 180, anchor= tk.CENTER)
        
        #Button to enter time on Timer window
        self.timer = tk.Button(self, text= "Enter", command= self.myClick)
        self.timer.place(x= 220, y= 220, anchor= tk.CENTER)

        #Button to switch to the To DO List from Timer window
        self.toDoList = tk.Button(self, text= "To Do List", command= None) # ToDo add a function to create a ToDo List Window
        self.toDoList.place(x= 0, y= 0 )
        
    
    #Function of Timer button
    def myClick(self): #Command for inputted data for the Timer
        try:  ##Converting time entered
            temp = int(self.hour.get())*3600 + int(self.minute.get())*60 + int(self.second.get())
        except:
            messagebox.showerror("Error", "Enter a valid integer")
            return
        
        while temp >-1:
            mins, secs = divmod(temp, 60)
            hours = 0
            if mins > 60:
                hours, mins = divmod(mins, 60)
            
            self.hour.set("{0:2d}".format(hours))
            self.minute.set("{0:2d}".format(mins))
            self.second.set("{0:2d}".format(secs))
        
            #Updating the time
            self.update()
            sleep(1)
        
            #MessageBox for the "Timer Stopped"
            if (temp == 0):
                messagebox.showinfo("", "Timer Stopped")
            temp -= 1
        


window_one: windowOne = windowOne()
window_one.mainloop()