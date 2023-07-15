"""
This modules produces the register window of the application

Author: Kevin Sunil

"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import utils
import application

class RegisterWindow(tk.Frame):
    """Class representing the registration window."""
    def __init__(self, master, db_manager):
        """
        Initialize the RegisterWindow.

        Args:
            master (tk.Tk): The root window.
            db_manager (utils.DBManager): The database manager instance.
        """
        super().__init__(master)
        self.master = master
        self.db_manager = db_manager
        self.master.title("Register")
        self.master.resizable(False, False)
        utils.center_window(240, 140, master)
        
        ttk.Label(self, text="Username:").grid(row=0, column=0)
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(self, text="Password:").grid(row=1, column=0)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        submit_button = ttk.Button(self, text="Submit", width=8, command=self.submit)
        submit_button.grid(row=2, column=1, sticky="e", padx=10, pady=(10, 0))

        submit_button = ttk.Button(self, text="Back", width=8, command=self.back)
        submit_button.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
        self.pack()
            
    def submit(self):
        """Submit the registration form."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if self.db_manager.register_user(username, password):
            print("Registered Successfully")
            self.user = username
            for widget in self.winfo_children(): 
                widget.destroy()
            self.destroy()
            application.Application(self.master, self.db_manager)
        else:
            messagebox.showinfo(title="Register", message="Username already taken")
            print("Username already taken")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def back(self):
        """Go back to the previous screen."""
        for widget in self.winfo_children(): 
            widget.destroy()
        self.destroy()
        application.Application(self.master, self.db_manager)
