import tkinter as Tk
from tkinter import *

##Main window of Productivity App setup
window = Tk()
window.title("Productivity App")
window.resizable(width= True, height= True)


#Creating label widgets
appTitle = Label(window, text = "Productivity App")
appTitle.grid(row=0, column=5)


#Function for TO DO LIST button on main window
def switch(): 
    toDoList = Label(window)
    toDoList.grid(row=2, column=5)
    
#Function for TIMER button on main window
def time():
    timer_main = Label(window)
    timer_main.grid(row= 4, column=5)
    

#Button on Main window for TO DO LIST
toDoList = Button(window, text= "To Do List", command= switch)
toDoList.grid(row=2, column=5)

#Button on main window for TIMER
timer_main = Button(window, text= "Timer", command=time)
timer_main.grid(row=4, column=5)




window.mainloop()
