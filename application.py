"""
This program represents a basic GUI application for PatCare. It provides a login, register, and reset password functionality.

Author: Kevin Sunil

"""

import tkinter as tk
from tkinter import ttk
import utils
import registerWindow
import loginWindow
import resetWindow


class Application(tk.Frame):
    """
    The main application class for PatCare.
    """

    def __init__(self, master, db_manager):
        """
        Initialize the Application.

        Args:
            master (tk.Tk): The root Tkinter window.
            db_manager: The database manager object.
        """
        super().__init__(master)
        self.master = master
        self.master.title("PatCare")
        utils.center_window(300, 190, master)
        self.db_manager = db_manager

        self.create_widgets()


    def create_widgets(self):
        """
        Create the widgets and layout for the application.
        """
        login_button = ttk.Button(
            self,
            text="Login",
            width=10,
            command=self.login
        )
        login_button.pack(padx=20, pady=(30, 10))

        register_button = ttk.Button(
            self,
            text="Register",
            width=10,
            command=self.register
        )
        register_button.pack(pady=10)

        reset_button = ttk.Button(
            self,
            text="Reset",
            width=10,
            command=self.reset_password
        )
        reset_button.pack(pady=10)

        self.pack()


    def login(self):
        """
        Destroy current widgets and open the login window.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        loginWindow.LoginWindow(self.master, self.db_manager)


    def register(self):
        """
        Destroy current widgets and open the register window.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        registerWindow.RegisterWindow(self.master, self.db_manager)


    def reset_password(self):
        """
        Destroy current widgets and open the reset password window.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        resetWindow.ResetWindow(self.master, self.db_manager)
