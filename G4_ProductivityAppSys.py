"""Author: Venise Saron & Suzette Irizarry
Professor: Raymond Storer
Subject: SDEV220
Last Revised: 3-7-2024
Purpose: This program is a GUI application
of a 'Productivity App System' complete with
a Main Window, To-Do App, and Timer App."""

# Import the necessary modules
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from time import sleep
import customtkinter as ctk
from PIL import ImageTk, Image
import sqlite3

# Setting up dark/light mode by default
ctk.set_appearance_mode("light")


class MainWindow(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.geometry("1000x600")
        self.resizable(False, False)  # Sets the window to be non-resizable
        self.title("Productivity App System")

        """Displays a background image for the main window"""
        self.background_img = ImageTk.PhotoImage(Image.open("images/main.jpeg"))
        self.background_label = Label(self, image=self.background_img, bg="white")
        self.background_label.pack()

        """Create a border frame for label and button widgets"""
        self.border_frame = ctk.CTkFrame(self.background_label, width=600, height=500,
                                         fg_color="pink")
        self.border_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        """Add labels for main header
        and a subheading"""
        self.main_heading = ctk.CTkLabel(self.border_frame, text="Productivity App",
                                         font=ctk.CTkFont("Arial", size=40))
        self.main_heading.place(x=160, y=45)

        self.main_subheading = ctk.CTkLabel(self.border_frame, text="How will you choose to start your day?",
                                            font=ctk.CTkFont("Arial", size=18, slant="italic"),
                                            fg_color="transparent")
        self.main_subheading.place(x=150, y=120)

        """Create button that will
        navigate to the To-Do App Window"""
        self.todo_button = ctk.CTkButton(self.border_frame, text="To-Do List", width=180, corner_radius=10,
                                         font=ctk.CTkFont("Arial", size=28), fg_color="black",
                                         hover_color="gray", text_color="white", command=self.todo_command)
        self.todo_button.place(x=210, y=230)

        """Create button that will
        navigate to the Timer App Window"""
        self.timer_button = ctk.CTkButton(self.border_frame, text="Timer", width=180, corner_radius=10,
                                          font=ctk.CTkFont("Arial", size=28), fg_color="black",
                                          hover_color="gray", text_color="white", command=self.timer_command)
        self.timer_button.place(x=210, y=330)

    """Define commands"""

    def todo_command(self):
        """Method for displaying the To-Do List window"""
        todo_window = ToDoApp(self)

    def timer_command(self):
        """Method for displaying the Timer window"""
        timer_window = TimerApp(self)


class ToDoApp(tk.Toplevel):
    """Displays the to-do application page."""

    def __init__(self, master):
        super().__init__(master)

        self.geometry("1050x900")
        self.resizable(False, False)
        self.title("To-Do Application")

        """Display a background image
        for the to-do application window"""
        self.background_img = ImageTk.PhotoImage(Image.open("images/bkgrnd.jpeg"))
        self.background_label = Label(self, image=self.background_img, bg="white")
        self.background_label.pack()

        """Create button that will
        navigate to timer application 
        outside the main frame"""

        self.timer_button = ctk.CTkButton(self, text="Timer", width=110, corner_radius=6,
                                          font=ctk.CTkFont("Arial", size=20), fg_color="black",
                                          hover_color="gray", text_color="white", command=self.timer_command())
        self.timer_button.place(x=480, y=830)

        """Create database or connect 
        to existing one"""
        self.conn = sqlite3.connect('tasks.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                                (id INTEGER PRIMARY KEY, task TEXT)''')
        self.conn.commit()

        """Create a mainframe
        that will hold the rest of the widgets"""
        self.main_frame = ctk.CTkFrame(self.background_label, width=800, height=650,
                                       fg_color="white", bg_color="black", corner_radius=30)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        """Add labels for main header"""
        self.heading = ctk.CTkLabel(self.main_frame, text="To-Do List", font=ctk.CTkFont("Arial", size=48))
        self.heading.place(x=290, y=45)

        """Create scrollable frame"""
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=700, height=430, corner_radius=10,
                                                       fg_color="black", scrollbar_fg_color="black")
        self.scrollable_frame.place(x=160, y=280)

        """Create an entry widget
        within scrollable frame"""
        self.user_entry = ctk.CTkEntry(self.scrollable_frame, placeholder_text="Type your task here...",
                                       placeholder_text_color="black", corner_radius=10,
                                       font=ctk.CTkFont("Arial", size=18, slant="italic"),
                                       border_color="white", height=40)
        self.user_entry.pack(fill="x")

        """Create a frame where initial
        tasks are placed inside the
        not completed category"""
        self.todo_frame = ctk.CTkFrame(self.scrollable_frame, height=370,
                                       fg_color="white", corner_radius=10)
        self.task_listbox = Listbox(self.todo_frame, width=70, height=15,
                                    font=("Arial", 16), justify="center",
                                    selectbackground="gray", selectmode="single")

        # Place the frame, and listbox
        self.todo_frame.pack(pady=10, fill="x")
        self.task_listbox.place(x=30, y=30)

        """Add a functional button for adding tasks"""
        self.add_button = ctk.CTkButton(self.scrollable_frame, text="Add Task", width=120,
                                        corner_radius=6, font=ctk.CTkFont("Arial", size=16),
                                        fg_color="black", hover_color="gray", bg_color="white",
                                        text_color="white", command=self.add_task)
        self.add_button.place(x=570, y=6)

        """Add a functional button that when
        clicked, will delete selected task"""
        self.del_button = ctk.CTkButton(self.todo_frame, text="Delete", width=100,
                                        corner_radius=6, font=ctk.CTkFont("Arial", size=18),
                                        fg_color="black", hover_color="gray",
                                        text_color="white", command=self.delete_task)
        self.del_button.place(x=160, y=330)

        """Adds a functional button that implements
        the 'refresh_list method', which displays 
        an up-to-date list of tasks from the database"""
        self.refresh_button = ctk.CTkButton(self.todo_frame, text="Refresh List", width=130,
                                            corner_radius=6, font=ctk.CTkFont("Arial", size=18),
                                            fg_color="black", hover_color="gray",
                                            text_color="white", command=self.refresh_list)
        self.refresh_button.place(x=400, y=330)

        # Populate task list
        self.refresh_list()

    """List of defined commands"""

    def add_task(self):
        """This command takes initial task input
        and contains it within the task box"""
        task = self.user_entry.get()
        if task:
            self.c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
            self.conn.commit()
            self.user_entry.delete(0, ctk.END)
            self.refresh_list()
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def refresh_list(self):
        self.task_listbox.delete(0, ctk.END)
        self.c.execute("SELECT * FROM tasks")
        tasks = self.c.fetchall()
        for task in tasks:
            self.task_listbox.insert(ctk.END, task[1])

    def delete_task(self):
        """This command deletes selected task input
        contained within the task box"""
        try:
            selected_index = self.task_listbox.curselection()[0]
            selected_task = self.task_listbox.get(selected_index)
            self.c.execute("DELETE FROM tasks WHERE task=?", (selected_task,))
            self.conn.commit()
            self.refresh_list()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

    def __del__(self):
        self.conn.close()

    def timer_command(self):
        """Method for displaying the Timer window"""
        timer_window = TimerApp(self)


class TimerApp(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Timer Countdown")
        self.geometry("500x500")

        # Background image for Timer
        self.background_image = Image.open("images/IMG_5141.JPG")

        # Resizing image to match window size
        self.background_image = self.background_image.resize((500, 500))

        # Label to display background image for Timer
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(x=0, y=0)

        # Creating label widgets
        self.timerTitle = tk.Label(self, text="Timer")
        self.timerTitle.place(x=220, y=100, anchor=tk.CENTER)

        # Variables that show the time with default value
        self.hour = tk.StringVar(value="00")
        self.minute = tk.StringVar(value="00")
        self.second = tk.StringVar(value="00")

        # Take user input
        self.hourEntry = tk.Entry(self, width=3, textvariable=self.hour)
        self.hourEntry.place(x=170, y=180, anchor=tk.CENTER)

        self.minuteEntry = tk.Entry(self, width=3, textvariable=self.minute)
        self.minuteEntry.place(x=220, y=180, anchor=tk.CENTER)

        self.secondEntry = tk.Entry(self, width=3, textvariable=self.second)
        self.secondEntry.place(x=270, y=180, anchor=tk.CENTER)

        # Button to enter time on Timer window
        self.timer = tk.Button(self, text="Enter", command=self.myClick)
        self.timer.place(x=220, y=220, anchor=tk.CENTER)

        # Button to switch to the To DO List from Timer window
        self.toDoList = tk.Button(self, text="To Do List",
                                  command=self.todo_command)  # Function to open To-Do List Window
        self.toDoList.place(x=0, y=0)

    """Define commands"""

    def todo_command(self):
        """Method for displaying the To-Do List window"""
        todo_window = ToDoApp(self)

    # Function of Timer button
    def myClick(self):  # Command for inputted data for the Timer
        try:  # Converting time entered
            temp = int(self.hour.get()) * 3600 + int(self.minute.get()) * 60 + int(self.second.get())
        except:
            messagebox.showerror("Error", "Enter a valid integer")
            return

        while temp > -1:
            mins, secs = divmod(temp, 60)
            hours = 0
            if mins > 60:
                hours, mins = divmod(mins, 60)

            self.hour.set("{0:2d}".format(hours))
            self.minute.set("{0:2d}".format(mins))
            self.second.set("{0:2d}".format(secs))

            # Updating the time
            self.update()
            sleep(1)

            # MessageBox for the "Timer Stopped"
            if temp == 0:
                messagebox.showinfo("", "Timer Stopped")
            temp -= 1


"""Important!! Include the entry point for program execution"""
if __name__ == "__main__":
    startup = MainWindow()
    startup.mainloop()
