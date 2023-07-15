"""
This module produces the dashboard of admin user, once they logged

Author: Kevin Sunil

"""
import tkinter as tk
from tkinter import ttk
import admin
import utils
import viewWindow
import addWindow
import acceptWindow
import elevateWindow
import application

class AdminDashboard(tk.Frame):
    """
    AdminDashboard class represents the main dashboard for the admin user.
    
    """

    def __init__(self, master, db_manager, username):
        """
        Initializes the AdminDashboard object.

        Args:
            master (tkinter.Tk): The root window object.
            db_manager (DatabaseManager): The database manager object.
            username (str): The username of the admin user.
        """
        super().__init__(master)
        self.master = master
        self.db_manager = db_manager
        self.user = admin.Admin(username, db_manager)
        self.elevate = True
        if self.user.level == 5:
            self.elevate = False
        self.master.title(self.user.username)
        self.master.resizable(False, False)
        if self.elevate:
            utils.center_window(240, 250, master)
        else:
            utils.center_window(240, 350, master)

        # View Button
        view_button = ttk.Button(self, text="View", width=20, command=self.view)
        view_button.pack(padx=20, pady=(30, 10))

        # Add Button
        add_button = ttk.Button(self, text="Add", width=20, command=self.add)
        add_button.pack(pady=10)

        if self.elevate:
            # Request Elevation Button
            elevate_button = ttk.Button(self, text="Request Elevation", width=20, command=self.elevate_request)
            elevate_button.pack(pady=10)
        else:
            # Lock Data Button
            lock_button = ttk.Button(self, text="Lock Data", width=20, command=self.lock)
            lock_button.pack(pady=10)

            # Unlock Data Button
            unlock_button = ttk.Button(self, text="Unlock Data", width=20, command=self.unlock)
            unlock_button.pack(pady=10)

        # Accept Elevation Button
        accept_button = ttk.Button(self, text="Accept Elevation", width=20, command=self.accept_elevate)
        accept_button.pack(pady=10)

        # Logout Button
        logout_button = ttk.Button(self, text="Logout", width=20, command=self.logout)
        logout_button.pack(pady=10)

        self.pack()

    def view(self):
        """
        Callback function for the View button.
        Destroys the current window and opens the view window.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        viewWindow.ViewWindow(self.master, self.db_manager, self.user, self.user.level)

    def add(self):
        """
        Callback function for the Add button.
        Destroys the current window and opens the add window.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        addWindow.AddWindow(self.master, self.db_manager, self.user)

    def elevate_request(self):
        """
        Callback function for the Request Elevation button.
        Destroys the current window and opens the elevate window.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        elevateWindow.ElevateWindow(self.master, self.db_manager, self.user)

    def lock(self):
        """
        Sets the lock status of the user in the database to 1 (locked).
        """
        self.db_manager.set_lock(self.user.username, 1)

    def unlock(self):
        """
        Sets the lock status of the user in the database to 0 (unlocked).
        """
        self.db_manager.set_lock(self.user.username, 0)

    def accept_elevate(self):
        """
        Callback function for the Accept Elevation button.
        Destroys the current window and opens the accept elevation window.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        acceptWindow.AcceptWindow(self.master, self.db_manager, self.user)

    def logout(self):
        """
        Callback function for the Logout button.
        Destroys the current window and opens the application window.
        """
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        application.Application(self.master, self.db_manager)