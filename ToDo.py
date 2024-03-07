"""This is the to-do application window
that is linked to the main window"""

from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
from PIL import ImageTk, Image
import sqlite3

ctk.set_appearance_mode("light")


class ToDoApp(ctk.CTk):
    """Displays the to-do application page."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.geometry("1050x900")
        self.resizable(False, False)
        self.title("To-Do Application")

        """Display a background image
        for the to-do application window"""
        self.background_img = ImageTk.PhotoImage(Image.open("images/bkgrnd.jpeg"))
        self.background_label = Label(self, image=self.background_img, bg="white")
        self.background_label.pack()

        """Create button that will
        go back to main page outside
        the main frame"""
        self.back_button = ctk.CTkButton(self, text="Main", width=110, corner_radius=6,
                                         font=ctk.CTkFont("Arial", size=20), fg_color="black",
                                         hover_color="gray", text_color="white")
        self.back_button.place(x=40, y=40)

        """Create button that will
        navigate to timer application 
        outside the main frame"""
        self.timer_button = ctk.CTkButton(self, text="Timer", width=110, corner_radius=6,
                                          font=ctk.CTkFont("Arial", size=20), fg_color="black",
                                          hover_color="gray", text_color="white")
        self.timer_button.place(x=880, y=830)

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

        """Add labels for main header 
        and a subhead"""
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

        # Place the frame, label, and listbox
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


if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
