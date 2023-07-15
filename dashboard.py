"""
This module is initialised once user is logged. It checks which type of user dashboard to launch and launches it

Author: Kevin Sunil

"""
import tkinter as tk
import adminDashboard
import userDashboard

class Dashboard(tk.Frame):
    """
    Represents a dashboard application.

    """

    def __init__(self, master, db_manager, username):
        """
        Initialize the dashboard.

        Args:
            master (tk.Tk): The root Tkinter window.
            db_manager: The database manager object.
        """
        super().__init__(master)
        
        # Check if the user is an admin
        if db_manager.is_admin(username):
            # Create an instance of the AdminDashboard class
            adminDashboard.AdminDashboard(master, db_manager, username)
        else:
            # Create an instance of the UserDashboard class
            userDashboard.UserDashboard(master, db_manager, username)
