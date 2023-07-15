"""
This module shows patient data in the datbase

Author: Kevin Sunil

"""

import tkinter as tk
from tkinter import ttk
import adminDashboard
import utils


class ViewWindow(tk.Frame):
    """
    A class representing the View Window of the application.

    """

    def __init__(self, master, db_manager, user, level):
        """
        Initializes the ViewWindow.

        Args:
            master (tk.Tk): The root window of the application.
            db_manager (DBManager): An instance of the DBManager class.
            user (User): An instance of the User class.
            level (int): The level of the user.

        """
        super().__init__(master)
        self.master = master
        self.master.title("View")
        self.db_manager = db_manager
        self.username = user.username
        self.level = level
        utils.center_window(40, 40, master)

        view = tk.Toplevel(self)
        view.transient(self)
        view.title('View all Data')
        view.protocol("WM_DELETE_WINDOW", self.disable_event)

        columns = ('Patient_ID', 'Name', 'Age', 'DateOfBirth', 'GPNumber', 'MaritalStatus', 'Height', 'Weight', 'BloodType', 'BloodPressure', 'BloodSugar', 'TestsTaken', 'OutpatientStatus')
        self.tree = ttk.Treeview(view, height=20, columns=columns, show='headings')
        self.tree.grid(row=0, column=0, sticky='news')

        # Setup columns attributes
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)

        data = []

        if self.level == 5:
            if self.db_manager.get_lock(self.username) == 0:
                data = self.db_manager.view_data(0)

        if not data:
            data = self.db_manager.view_data(1)

        # Populate data to treeview
        for rec in data:
            self.tree.insert('', 'end', value=rec)

        # Scrollbar
        self.sb = ttk.Scrollbar(view, orient=tk.VERTICAL, command=self.tree.yview)
        self.sb.grid(row=0, column=1, sticky='ns')
        self.tree.config(yscrollcommand=self.sb.set)

        back_button = ttk.Button(view, text="Back", width=8, command=self.back)
        back_button.grid(row=1, column=0, sticky="w", padx=10, pady=(10, 10))

    def disable_event(self):
        """
        Callback function to handle the disable event.

        """
        pass

    def back(self):
        """
        Performs actions to go back to the previous screen.

        """
        for widget in self.winfo_children():
            widget.destroy()

        self.destroy()
        self.tree.destroy()
        self.sb.destroy()

        adminDashboard.AdminDashboard(self.master, self.db_manager, self.username)
