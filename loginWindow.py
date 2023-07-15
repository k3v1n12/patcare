"""
This modules produces the login window of the application

Author: Kevin Sunil

"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import application
import dashboard
import utils


class LoginWindow(tk.Frame):
    """Represents the login window of the application."""

    def __init__(self, master, db_manager):
        """
        Initialize the LoginWindow.

        Args:
            master (tk.Tk): The parent Tkinter window.
            db_manager: The database manager object.
        """
        super().__init__(master)
        self.master = master
        self.db_manager = db_manager
        self.master.title("Login")
        self.master.resizable(False, False)
        utils.center_window(240, 130, master)

        ttk.Label(self, text="Username:").grid(row=0, column=0)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self, text="Password:").grid(row=1, column=0)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        submit_button = ttk.Button(self, text="Submit", width=8, command=self.submit)
        submit_button.bind('<Return>', self.return_pressed)
        submit_button.grid(row=2, column=1, sticky="e", padx=10, pady=(10, 0))

        submit_button = ttk.Button(self, text="Back", width=8, command=self.back)
        submit_button.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
        self.pack()

    def return_pressed(self, event):
        """Submit the login form when the Return key is pressed."""
        self.submit()

    def submit(self):
        """Handle the login submission."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.db_manager.login(username, password):
            print("Successful login")
            for widget in self.winfo_children():
                widget.destroy()
            self.destroy()
            dashboard.Dashboard(self.master, self.db_manager, username)
        else:
            messagebox.showinfo(title="Login", message="Unsuccessful login")
            print("Unsuccessful login")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def back(self):
        """Handle the back button click."""
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        application.Application(self.master, self.db_manager)

    def get_username(self):
        """Return the entered username."""
        return self.username_entry.get()
