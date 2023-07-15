"""
This module contains User class. 

Author: Kevin Sunil

"""
class User:
    """
    Represents a user in the system.
    """

    def __init__(self, username, db_manager):
        """
        Initializes a User instance.

        Args:
            username (str): The username of the user.
            db_manager (DBManager): An instance of the database manager.
        """
        self.username = username
        self.db_manager = db_manager
        self.level = 0
