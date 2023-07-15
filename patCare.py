"""
This main module initializes patCare using tkinter and connects to a database using the application and database modules.

Author: Kevin Sunil

"""

import application
import database
import tkinter as tk


def main():
    """
    The main function initializes the application and database, connects to the database,
    and starts the tkinter event loop.
    """
    # Initialize the database manager
    db_manager = database.Database()

    # Connect to the database
    db_manager.connect()

    # Initialize the root tkinter window
    root = tk.Tk()

    # Create an instance of the application
    app = application.Application(root, db_manager)

    # Start the tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()