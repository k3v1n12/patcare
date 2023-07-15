"""
This module handles all the database operations for the program

Author: Kevin Sunil

"""

import mysql.connector
import ast
from datetime import datetime

db_config = {
'host': 'localhost',
'user': 'root',
'password': 'uieuVuddLwRyB6F5r9uU',
'database': 'padcare'
}

class Database:
    """
    This class represents a database and provides methods to interact with it.
    """
    def __init__(self):
        """
        Initializes the Database object.
        """
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Connects to the MySQL database.
        """
        try:
            self.connection = mysql.connector.connect(**db_config)
            self.cursor = self.connection.cursor()
            self.create_table()
            self.check_table()

        except mysql.connector.Error as error:
            print("Database Error:", error)

    def disconnect(self):
        """
        Disconnects from the MySQL database.
        """
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def create_table(self):
        """
        Creates necessary tables in the database if they don't already exist.
        """
        self.cursor.execute("SHOW TABLES")
        temp = self.cursor.fetchall()
        tables = [item[0] for item in temp]

        if "users" not in tables:
            self.execute_query("""CREATE TABLE users(
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )""")

        if "admins" not in tables:
            self.execute_query("""CREATE TABLE admins(
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                level INT CHECK (level BETWEEN 1 AND 5),
                datalock BOOLEAN NOT NULL DEFAULT 1,
                request VARCHAR(255) DEFAULT ('[]')
            )""")
            
            self.execute_query("""INSERT INTO admins (username, password, level) 
                VALUES ('admin', 'admin', 5)""")
            
            

        if "personals" not in tables:
            self.execute_query("""CREATE TABLE personals (
                Patient_ID INT NOT NULL AUTO_INCREMENT,
                Name VARCHAR(255),
                Age INT,
                DateOfBirth DATE,
                GPNumber VARCHAR(255),
                PRIMARY KEY (Patient_ID)
            )""")

            self.execute_query("""CREATE TABLE dummies (
                Patient_ID INT NOT NULL,
                Name VARCHAR(255),
                Age INT,
                DateOfBirth DATE,
                GPNumber VARCHAR(255) UNIQUE,
                FOREIGN KEY (Patient_ID) REFERENCES personals(Patient_ID)
            )""")

        if "histories" not in tables:
            self.execute_query("""CREATE TABLE histories (
                Patient_ID INT NOT NULL,
                MaritalStatus VARCHAR(255),
                Height FLOAT,
                Weight FLOAT,
                BloodType VARCHAR(255),
                BloodPressure VARCHAR(255),
                BloodSugar FLOAT,
                TestsTaken VARCHAR(255),
                OutpatientStatus VARCHAR(255),
                FOREIGN KEY (Patient_ID) REFERENCES personals(Patient_ID)
            )""")

    def check_table(self):
        """
        Checks if the necessary constraints exist in the tables and creates them if not.
        """
        user_result = self.fetch_query("""SELECT CONSTRAINT_NAME
                            FROM 
                            INFORMATION_SCHEMA.TABLE_CONSTRAINTS
                            WHERE 
                            TABLE_SCHEMA = 'patcare'
                            AND TABLE_NAME = 'users'
                            AND CONSTRAINT_NAME = 'username_unique_user'
                        """)

        if user_result:
            self.execute_query("""ALTER TABLE users
                ADD CONSTRAINT username_unique_user 
                CHECK (username NOT IN (SELECT username FROM admins))
                """)

        admin_result = self.fetch_query("""SELECT CONSTRAINT_NAME
                            FROM 
                            INFORMATION_SCHEMA.TABLE_CONSTRAINTS
                            WHERE 
                            TABLE_SCHEMA = 'patcare'
                            AND TABLE_NAME = 'admins'
                            AND CONSTRAINT_NAME = 'username_unique_admin'
                        """)

        if admin_result:
            self.execute_query("""ALTER TABLE admins
                ADD CONSTRAINT username_unique_admin 
                CHECK (username NOT IN (SELECT username FROM users))
                """)

    def execute_query(self, query, values=None):
        """
        Executes a SQL query.
        
        Args:
            query (str): The SQL query to execute.
            values (tuple, optional): The values to substitute in the query. Defaults to None.
        
        Returns:
            bool: True if the query was executed successfully, False otherwise.
        """
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            print("Error executing query:", error)
            return False

    def fetch_query(self, query, values=None):
        """
        Fetches results of a SQL query.
        
        Args:
            query (str): The SQL query to execute.
            values (tuple, optional): The values to substitute in the query. Defaults to None.
        
        Returns:
            list: The fetched results as a list of tuples.
        """
        try:
            self.cursor.execute(query, values)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as error:
            print("Error fetching query results:", error)
            return None

    def login(self, username, password):
        """
        Performs login operation for a user or an admin.
        
        Args:
            username (str): The username.
            password (str): The password.
        
        Returns:
            bool: True if the login is successful, False otherwise.
        """
        if self.is_admin(username):
            return self.admin_login(username, password)

        return self.user_login(username, password)

    def admin_login(self, username, password):
        """
        Performs login operation for an admin.
        
        Args:
            username (str): The username.
            password (str): The password.
        
        Returns:
            bool: True if the login is successful, False otherwise.
        """
        query = "SELECT COUNT(*) FROM admins WHERE username = %s and password = %s"
        params = (username, password)
        result = self.fetch_query(query, params)
        if result[0][0] == 0:
            return False
        return True

    def user_login(self, username, password):
        """
        Performs login operation for a user.
        
        Args:
            username (str): The username.
            password (str): The password.
        
        Returns:
            bool: True if the login is successful, False otherwise.
        """
        query = "SELECT COUNT(*) FROM users WHERE username = %s and password = %s"
        params = (username, password)
        result = self.fetch_query(query, params)
        if result[0][0] == 0:
            return False
        return True

    def register_user(self, username, password):
        """
        Registers a new user.
        
        Args:
            username (str): The username.
            password (str): The password.
        
        Returns:
            bool: True if the registration is successful, False otherwise.
        """
        if self.is_user(username) or self.is_admin(username):
            return False

        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        params = (username, password)
        return self.execute_query(query, params)

    def register_admin(self, username, password, level):
        """
        Registers a new admin.
        
        Args:
            username (str): The username.
            password (str): The password.
            level (int): The admin level.
        """
        query = "INSERT INTO admins (username, password, level) VALUES (%s, %s, %s)"
        params = (username, password, level)
        self.execute_query(query, params)

    def reset_password(self, username, password, new_password):
        """
        Resets the password for a user or an admin.
        
        Args:
            username (str): The username.
            password (str): The current password.
            new_password (str): The new password.
        
        Returns:
            bool: True if the password is reset successfully, False otherwise.
        """
        if self.is_admin(username):
            if self.admin_login(username, password):
                return self.reset_admin_password(username, new_password)
        elif self.user_login(username, password):
            return self.reset_user_password(username, new_password)
        return False

    def reset_user_password(self, username, new_password):
        """
        Resets the password for a user.
        
        Args:
            username (str): The username.
            new_password (str): The new password.
        
        Returns:
            bool: True if the password is reset successfully, False otherwise.
        """
        query = "UPDATE users SET password = %s WHERE username = %s"
        params = (new_password, username)
        return self.execute_query(query, params)

    def reset_admin_password(self, username, new_password):
        """
        Resets the password for an admin.
        
        Args:
            username (str): The username.
            new_password (str): The new password.
        
        Returns:
            bool: True if the password is reset successfully, False otherwise.
        """
        query = "UPDATE admins SET password = %s WHERE username = %s"
        params = (new_password, username)
        return self.execute_query(query, params)

    def get_admin_list(self, level):
        """
        Retrieves a list of admins with a level higher than the specified level.
        
        Args:
            level (int): The level threshold.
        
        Returns:
            list: A list of admin usernames.
        """
        query = "SELECT username FROM admins WHERE level > %s"
        params = (level,)
        result = self.fetch_query(query, params)
        return result

    def get_admin_level(self, username):
        """
        Retrieves the level of an admin.
        
        Args:
            username (str): The admin username.
        
        Returns:
            int: The admin level.
        """
        query = "SELECT level FROM admins WHERE username = %s"
        params = (username,)
        result = self.fetch_query(query, params)
        if result:
            return result[0][0]
        else:
            return 0

    def send_elevate_request(self, selected_admin, current_user):
        """
        Sends an elevate request from a user to an admin.
        
        Args:
            selected_admin (str): The admin username.
            current_user (str): The current user.
        
        Returns:
            bool: True if the request is sent successfully, False otherwise.
        """
        query = "SELECT request FROM admins WHERE username = %s"
        params = (selected_admin,)
        result = self.fetch_query(query, params)
        request = result[0][0]
        request = ast.literal_eval(request)
        request = [n.strip() for n in request]
        if current_user not in request:
            request.append(current_user)
            query = "UPDATE admins SET request = %s WHERE username = %s"
            requestString = "{}".format(request)
            print(requestString)
            params = (requestString, selected_admin)
            return self.execute_query(query, params)

        return True

    def get_request_list(self, username):
        """
        Retrieves the request list for an admin.
        
        Args:
            username (str): The admin username.
        
        Returns:
            list: A list of usernames that sent elevation requests.
        """
        query = "SELECT request FROM admins WHERE username = %s"
        params = (username,)
        result = self.fetch_query(query, params)
        request = result[0][0]
        request = ast.literal_eval(request)
        request = [n.strip() for n in request]
        return request

    def accept_elevate_request(self, selected_user, admin, level):
        """
        Accepts an elevation request for an admin.
        
        Args:
            selected_user (str): The username of the user to be elevated.
            admin (str): The username of the admin who is elavating.
            level (int): The current admin level.
        """
        if level > 0:
            query = "UPDATE admins SET level = %s WHERE username = %s"
            params = (level + 1, selected_user)
            self.execute_query(query, params)
        else:
            query = "SELECT password FROM users WHERE username = %s"
            params = (selected_user,)
            password = self.fetch_query(query, params)
            password = password[0][0]
            
            query = "DELETE FROM users WHERE username = %s"
            params = (selected_user,)
            self.execute_query(query, params)

            query = "INSERT INTO admins (username, password, level) VALUES (%s, %s, %s)"
            params = (selected_user, password, level + 1)
            self.execute_query(query, params)
                   
        query = "SELECT request FROM admins WHERE username = %s"
        params = (admin,)
        result = self.fetch_query(query, params)
        request = result[0][0]
        request = ast.literal_eval(request)
        request = [n.strip() for n in request]
        request.remove(selected_user)
        query = "UPDATE admins SET request = %s WHERE username = %s"
        requestString = "{}".format(request)
        print(requestString)
        params = (requestString, admin)
        self.execute_query(query, params)

    def set_lock(self, admin, value):
        """
        Sets the data lock for an admin.
        
        Args:
            admin (str): The admin username.
            value (int): The lock value (0 or 1).
        """
        query = "UPDATE admins SET datalock = %s WHERE username = %s"
        params = (value, admin)
        self.execute_query(query, params)

    def get_lock(self, admin):
        """
        Retrieves the data lock status for an admin.
        
        Args:
            admin (str): The admin username.
        
        Returns:
            int: The lock status (0 or 1).
        """
        query = "SELECT datalock FROM admins WHERE username = %s"
        params = (admin,)
        result = self.fetch_query(query, params)
        return int(result[0][0])

    def is_admin(self, username):
        """
        Checks if a user is an admin.
        
        Args:
            username (str): The username.
        
        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        query = "SELECT COUNT(*) FROM admins WHERE username = %s"
        params = (username,)
        result = self.fetch_query(query, params)
        if result[0][0] == 0:
            return False
        return True

    def is_user(self, username):
        """
        Checks if a user is a regular user.
        
        Args:
            username (str): The username.
        
        Returns:
            bool: True if the user is a regular user, False otherwise.
        """
        query = "SELECT COUNT(*) FROM users WHERE username = %s"
        params = (username,)
        result = self.fetch_query(query, params)
        if result[0][0] == 0:
            return False
        return True

    def add_data(self, data):
        """
        Adds data to the database.
        
        Args:
            data (dict): The data to be added.
        """
        query = " INSERT INTO personals(Name, Age, DateOfBirth, GPNumber) VALUES(%s, %s, %s, %s) "

        date = datetime.strptime(data['dob'], '%d/%m/%Y').strftime('%Y-%m-%d')

        params = (data['name'], data['age'], date, data['gp'])
        self.execute_query(query, params)

        query = "SELECT Patient_ID FROM personals WHERE GPNumber = %s"
        print(data['gp'])
        params = (data['gp'],)

        id = self.fetch_query(query, params)
        id = id[0][0]

        query = " INSERT INTO dummies(Patient_ID, Name, Age, DateOfBirth, GPNumber) VALUES(%s, %s, %s, %s, %s) "
        params = (id, "Dummy", 22, "2022-12-12", "34534534")
        self.execute_query(query, params)

        query = """ INSERT INTO histories(Patient_ID, MaritalStatus, Height, Weight, BloodType, BloodPressure,
                    BloodSugar, TestsTaken, OutpatientStatus) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
        params = (
            id, data['marial'], data['height'], data['weight'], data['btype'], data['bp'], data['bsugar'],
            data['test'], data['status'])
        self.execute_query(query, params)

    def view_data(self, datalock):
        """
        Retrieves data from the database.
        
        Args:
            datalock (int): The data lock status.
        
        Returns:
            list: A list of retrieved data.
        """
        if datalock == 0:
            #query = "SELECT * FROM personals INNER JOIN histories ON personals.Patient_ID = histories.Patient_ID"
            query = """SELECT personals.Patient_ID, personals.Name, personals.Age, personals.DateofBirth,
                       personals.GPNumber, histories.MaritalStatus, histories.Height, histories.Weight,
                       histories.BloodType, histories.BloodPressure, histories.BloodSugar,
                       histories.TestsTaken, histories.OutpatientStatus 
                       FROM personals INNER JOIN histories ON personals.Patient_ID = histories.Patient_ID"""
        else:
            #query = "SELECT * FROM dummies INNER JOIN histories ON dummies.Patient_ID = histories.Patient_ID"
            query = """SELECT dummies.Patient_ID, dummies.Name, dummies.Age, dummies.DateofBirth,
                       dummies.GPNumber, histories.MaritalStatus, histories.Height, histories.Weight,
                       histories.BloodType, histories.BloodPressure, histories.BloodSugar,
                       histories.TestsTaken, histories.OutpatientStatus 
                       FROM dummies INNER JOIN histories ON dummies.Patient_ID = histories.Patient_ID"""

        return self.fetch_query(query)
