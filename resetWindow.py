"""
This modules produces the rest window of the application

Author: Kevin Sunil

"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import utils
import application

class ResetWindow(tk.Frame):
    """
    A class representing the reset window

    """

    def __init__(self, master, db_manager):
        """
        Initializes the ResetWindow.

        Args:
            master (tk.Tk): The root window of the application.
            db_manager (utils.DBManager): The database manager object.
        """
        super().__init__(master)
        self.master = master
        self.db_manager = db_manager
        self.master.title("Reset")
        self.master.resizable(False, False)
        utils.center_window(300, 180, master)

        ttk.Label(self, text="Username:").grid(row=0, column=0)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self, text="Current Password:").grid(row=1, column=0)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self, text="New Password:").grid(row=2, column=0)
        self.new_password_entry = ttk.Entry(self, show="*")
        self.new_password_entry.grid(row=2, column=1, padx=10, pady=10)

        submit_button = ttk.Button(self, text="Submit", width=8, command=self.submit)
        submit_button.grid(row=3, column=1, sticky="e", padx=10, pady=(10, 0))

        submit_button = ttk.Button(self, text="Back", width=8, command=self.back)
        submit_button.grid(row=3, column=0, sticky="w", padx=10, pady=(10, 0))
        self.pack()

    def submit(self):
        """
        Handles the submit button click event.
        Resets the password if the username and current password match.
        Displays appropriate messages based on the result.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        new_password = self.new_password_entry.get()

        if self.db_manager.reset_password(username, password, new_password):
            print("Password successfully reset")
            for widget in self.winfo_children():
                widget.destroy()
            self.destroy()
            application.Application(self.master, self.db_manager)
        else:
            messagebox.showinfo(title="Reset", message="Incorrect username or Password")
            print("Incorrect username or Password")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.new_password_entry.delete(0, tk.END)

    def back(self):
        """
        Handles the back button click event.
        Destroys the current window and returns to the previous application window.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        application.Application(self.master, self.db_manager)

    def get_username(self):
        """
        Returns the username entered in the window.

        Returns:
            str: The username entered in the window.
        """
        return self.username_entry.get()
