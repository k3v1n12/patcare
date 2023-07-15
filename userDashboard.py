"""
This module produces the dashboard of admin user, once they logged

Author: Kevin Sunil

"""
import tkinter as tk
from tkinter import ttk
import user
import utils
import viewWindow
import elevateWindow
import application


class UserDashboard(tk.Frame):
    """
    Represents a user dashboard GUI.

    """

    def __init__(self, master, db_manager, username):
        """
        Initializes the UserDashboard class.

        Args:
            master (tk.Tk): The parent window.
            db_manager (object): The database manager object.
            username (str): The username of the user.
        """
        super().__init__(master)
        self.master = master
        self.db_manager = db_manager
        self.user = user.User(username, db_manager)
        self.master.title(self.user.username)
        self.master.resizable(False, False)
        utils.center_window(240, 150, master)

        view_button = ttk.Button(self, text="View", width=20, command=self.view)
        view_button.pack(padx=20, pady=(30, 10))

        elevate_button = ttk.Button(self, text="Request Elevation", width=20, command=self.elevate_request)
        elevate_button.pack(pady=10)

        logout_button = ttk.Button(self, text="Logout", width=20, command=self.logout)
        logout_button.pack(pady=10)

        self.pack()

    def view(self):
        """
        Callback function for the "View" button.
        Destroys the current window and opens the view window.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        viewWindow.ViewWindow(self.master, self.db_manager, self.user, self.user.level)

    def elevate_request(self):
        """
        Callback function for the "Request Elevation" button.
        Destroys the current window and opens the elevate window.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        elevateWindow.ElevateWindow(self.master, self.db_manager, self.user)

    def logout(self):
        """
        Callback function for the "Logout" button.
        Destroys the current window and opens the application window.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        application.Application(self.master, self.db_manager)
