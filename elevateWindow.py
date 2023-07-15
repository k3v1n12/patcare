"""
This is a module that creates a window for requesting elevation to an administrator.

Author: Kevin Sunil

"""

import tkinter as tk
from tkinter import ttk
import adminDashboard
import userDashboard

class ElevateWindow(tk.Frame):
    """
    A class representing the window for requesting elevation to an administrator.

    """

    def __init__(self, master, db_manager, user):
        """
        Initializes the ElevateWindow object.

        Args:
            master (tkinter.Tk): The root window object.
            db_manager (DatabaseManager): The database manager object.
            user (object): The user object.
        """
        super().__init__(master)
        self.master = master
        self.username = user.username
        self.level = user.level
        self.master.title("Elevate Request")
        self.db_manager = db_manager

        # Get admin list
        adminCollection = db_manager.get_admin_list(self.level)
        adminlist = []
        for admin in adminCollection:
            if self.username != admin[0]:
                adminlist.append(admin[0])

        var = tk.Variable(value=adminlist)

        # Create listbox widget
        self.listbox = tk.Listbox(
            master,
            listvariable=var,
            height=6,
            selectmode=tk.SINGLE
        )
        self.listbox.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        # Create scrollbar widget
        self.scrollbar = ttk.Scrollbar(
            master,
            orient=tk.VERTICAL,
            command=self.listbox.yview
        )
        self.listbox['yscrollcommand'] = self.scrollbar.set
        self.scrollbar.pack(side=tk.LEFT, expand=True, fill=tk.Y)

        # Bind event handler
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)

    def items_selected(self, event):
        """
        Event handler for the selection of items in the listbox.

        Args:
            event (tk.Event): The event object.

        """
        # Get selected indices
        selected_indices = self.listbox.curselection()
        # Get selected items
        selected_user = ",".join([self.listbox.get(i) for i in selected_indices])

        # Send elevate request to admin
        self.db_manager.send_elevate_request(selected_user, self.username)

        # Cleanup and destroy the current window
        self.listbox.unbind('<<ListboxSelect>>')
        self.listbox.destroy()
        self.scrollbar.destroy()
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()

        # Create admin or user dashboard based on the level
        if self.level > 0:
            adminDashboard.AdminDashboard(self.master, self.db_manager, self.username)
        else:
            userDashboard.UserDashboard(self.master, self.db_manager, self.username)
