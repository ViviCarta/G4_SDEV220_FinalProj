import tkinter as Tk
from tkinter import *

#Timer window setup
window = Tk()
window.title("Timer")
window.resizable(width= True, height= True)

#Creating label widgets
timerTitle = Label(window, text = "Timer")
timerTitle.grid(row=0, column=5)

#Function of Timer button
def myClick(): #Command for inputted data for the Timer
    timer = Label(window)
    timer.grid(row=2, column=5)
    

#Buttons on Timer window
timer = Button(window, text= "Enter", command= myClick)
timer.grid(row=2, column=5)

window.mainloop()