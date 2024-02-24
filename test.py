import tkinter as tk
from tkinter import messagebox
import sqlite3
from customtkinter import CustomTkinter


class ToDoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do App")

        # Create database or connect to existing one
        self.conn = sqlite3.connect('todo.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                        (id INTEGER PRIMARY KEY, task TEXT)''')
        self.conn.commit()

        # Initialize GUI components using CustomTkinter
        self.custom = CustomTkinter(master)
        self.task_entry = self.custom.Entry(master, width=40)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        self.add_button = self.custom.Button(master, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=1, padx=5, pady=10)

        self.task_listbox = self.custom.Listbox(master, width=50)
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.delete_button = self.custom.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=0, padx=5, pady=5, sticky='w')

        self.refresh_button = self.custom.Button(master, text="Refresh List", command=self.refresh_list)
        self.refresh_button.grid(row=2, column=1, padx=5, pady=5, sticky='e')

        # Populate task list
        self.refresh_list()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
            self.conn.commit()
            self.task_entry.delete(0, tk.END)
            self.refresh_list()
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def refresh_list(self):
        self.task_listbox.delete(0, tk.END)
        self.c.execute("SELECT * FROM tasks")
        tasks = self.c.fetchall()
        for task in tasks:
            self.task_listbox.insert(tk.END, task[1])

    def delete_task(self):
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


def main():
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
