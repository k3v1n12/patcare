"""
This module selects user from of list of user. The selects user will have his level elevated

Author: Kevin Sunil

"""
import tkinter as tk
from tkinter import ttk
import adminDashboard


class AcceptWindow(tk.Frame):
    """Represents a window for accepting requests."""

    def __init__(self, master, db_manager, user):
        """
        Initializes the AcceptWindow.

        Args:
            master (tk.Tk): The parent Tkinter window.
            db_manager (DatabaseManager): The database manager object.
            user (Admin): The admin object.

        """
        super().__init__(master)
        self.master = master
        self.master.title("Accept Request")
        self.username = user.username
        self.level = user.level
        self.db_manager = db_manager

        # Get the list of admin requests from the database manager
        admin_list = db_manager.get_request_list(self.username)
        print(admin_list)

        # Create a Tkinter variable and assign it the admin_list
        var = tk.Variable(value=admin_list)

        # Create a listbox widget and display the admin_list
        self.listbox = tk.Listbox(
            master,
            listvariable=var,
            height=6,
            selectmode=tk.SINGLE
        )
        self.listbox.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        # Link a scrollbar to the listbox
        self.scrollbar = ttk.Scrollbar(
            master,
            orient=tk.VERTICAL,
            command=self.listbox.yview
        )
        self.listbox['yscrollcommand'] = self.scrollbar.set
        self.scrollbar.pack(side=tk.LEFT, expand=True, fill=tk.Y)
        self.listbox.bind('<<ListboxSelect>>', self.items_selected)

    def items_selected(self, event):
        """
        Handles the event when items are selected in the listbox.

        Args:
            event (tk.Event): The event object.

        """
        # Get the selected indices
        selected_indices = self.listbox.curselection()

        # Get the selected items
        selected_user = ",".join([self.listbox.get(i) for i in selected_indices])

        # Check if the selected user is an admin
        if self.db_manager.is_admin(selected_user):
            level = self.db_manager.get_admin_level(selected_user)
        else:
            level = 0

        # Accept the elevate request for the selected user
        self.db_manager.accept_elevate_request(selected_user, self.username, level)

        # Clean up the GUI elements
        self.listbox.destroy()
        self.scrollbar.destroy()
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()

        # Open the admin dashboard
        adminDashboard.AdminDashboard(self.master, self.db_manager, self.username)
