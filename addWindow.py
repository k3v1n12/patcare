"""
This module takes input and submit patient data to database

Author: Kevin Sunil

"""
import tkinter as tk
import adminDashboard
from tkinter import ttk
import utils

class AddWindow(tk.Frame):
    """Class representing the 'Add' window for data entry."""

    def __init__(self, master, db_manager, user):
        """
        Initialize the AddWindow.

        Args:
            master (tk.Tk): The root Tkinter window.
            db_manager (DatabaseManager): The database manager object.
            user (User): The user object.

        """
        super().__init__(master)
        self.master = master
        self.master.title("Add")
        utils.center_window(310, 550, master)
        self.db_manager = db_manager
        self.username = user.username
        
        # Label and entry for name
        ttk.Label(self, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(self, width=26)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        
        # Label and entry for age
        tk.Label(self, text="Age:").grid(row=1, column=0, sticky="w")
        self.age_entry = tk.Entry(self, width=26)
        self.age_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        
        # Label and entry for date of birth
        tk.Label(self, text="DOB(dd/mm/yyyy):").grid(row=2, column=0, sticky="w")
        self.dob_entry = tk.Entry(self, width=26)
        self.dob_entry.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        # Label and entry for GP number
        tk.Label(self, text="GP Number:").grid(row=3, column=0, sticky="w")
        self.gp_entry = tk.Entry(self, width=26)
        self.gp_entry.grid(row=3, column=1, padx=10, pady=10, sticky="e")
        
        # Label and entry for marital status
        tk.Label(self, text="Marital Status:").grid(row=4, column=0, sticky="w")
        self.marital_entry = tk.Entry(self, width=26)
        self.marital_entry.grid(row=4, column=1, padx=10, pady=10, sticky="e")
        
        # Label and entry for height
        tk.Label(self, text="Height:").grid(row=5, column=0, sticky="w")
        self.height_entry = tk.Entry(self, width=26)
        self.height_entry.grid(row=5, column=1, padx=10, pady=10, sticky="e")
        
        # Label and entry for weight
        tk.Label(self, text="Weight:").grid(row=6, column=0, sticky="w")
        self.weight_entry = tk.Entry(self, width=26)
        self.weight_entry.grid(row=6, column=1, padx=10, pady=10, sticky="e")
        
        # Label and entry for blood type
        tk.Label(self, text="Blood Type:").grid(row=7, column=0, sticky="w")
        self.btype_entry = tk.Entry(self, width=26)
        self.btype_entry.grid(row=7, column=1, padx=10, pady=10, sticky="e")
        
        # Label and entry for blood pressure
        tk.Label(self, text="Blood Pressure:").grid(row=8, column=0, sticky="w")
        self.bp_entry = tk.Entry(self, width=26)
        self.bp_entry.grid(row=8, column=1, padx=10, pady=10, sticky="e")
        
        # Label and entry for blood sugar
        tk.Label(self, text="Blood Sugar:").grid(row=9, column=0, sticky="w")
        self.bsugar_entry = tk.Entry(self, width=26)
        self.bsugar_entry.grid(row=9, column=1, padx=10, pady=10, sticky="e")
        
        # Label and entry for test taken
        tk.Label(self, text="Test Taken:").grid(row=10, column=0, sticky="w")
        self.test_entry = tk.Entry(self, width=26)
        self.test_entry.grid(row=10, column=1, padx=10, pady=10, sticky="e")
        
        # Label and entry for OP status
        tk.Label(self, text="OP Status:").grid(row=11, column=0, sticky="w")
        self.status_entry = tk.Entry(self, width=26)
        self.status_entry.grid(row=11, column=1, padx=10, pady=10, sticky="e")
        
        # Submit button
        submit_button = tk.Button(self, text="Submit", width=8, command=self.submit)
        submit_button.grid(row=12, column=1, padx=10, pady=10, sticky="e")

        # Back button
        back_button = tk.Button(self, text="Back", width=8, command=self.back)
        back_button.grid(row=12, column=0, sticky="w", padx=10, pady=(10, 10))
        self.pack()
    
    def submit(self):
        """Submit the entered data."""
        data = {}
        data["name"] = self.name_entry.get()
        data["age"] = int(self.age_entry.get())
        data["dob"] = self.dob_entry.get()
        data["gp"] = self.gp_entry.get()
        data["marital"] = self.marital_entry.get()
        data["height"] = float(self.height_entry.get())
        data["weight"] = float(self.weight_entry.get())
        data["btype"] = self.btype_entry.get()
        data["bp"] = self.bp_entry.get()
        data["bsugar"] = float(self.bsugar_entry.get())
        data["test"] = self.test_entry.get()
        data["status"] = self.status_entry.get()
        
        self.db_manager.add_data(data)
        
        # Clear all entry fields
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.gp_entry.delete(0, tk.END)
        self.marital_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.btype_entry.delete(0, tk.END)
        self.bsugar_entry.delete(0, tk.END)
        self.test_entry.delete(0, tk.END)
        self.status_entry.delete(0, tk.END)
        self.bp_entry.delete(0, tk.END)
        
    def back(self):
        """Go back to the admin dashboard."""
        # Destroy all child widgets and the window itself
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        adminDashboard.AdminDashboard(self.master, self.db_manager, self.username)
