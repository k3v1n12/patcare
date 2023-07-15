"""
This module contains Admin class. 

Author: Kevin Sunil

"""
from user import User

class Admin(User):
    """
    Represents an administrator user with extended privileges.
    """

    def __init__(self, username, db_manager):
        """
        Initializes an Admin instance.

        Args:
            username (str): The username of the administrator.
            db_manager (DBManager): The database manager object.
        """
        super().__init__(username, db_manager)
        self.level = db_manager.get_admin_level(username)
        self.requests = []
        self.locked = True
