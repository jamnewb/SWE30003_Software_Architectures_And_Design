import os
import mysql.connector
import mysql
from connect_database import getDatabase

class AccountSystem:
    def __init__(self):
        self.onAccountPage = False
        self.onLoginPage = False
        self.onCreatePage = False
        self.dbHost = ""
        self.dbUser = ""
        self.dbPwd = ""
        self.dbSqlDb = ""

    def login(self):
        self.onLoginPage = True
        while self.onLoginPage:
            username = input("\nPlease enter your username. Enter 'back' to go to the account page.\n")
            if username == "back":
                self.onLoginPage = False
                return
            if username == "":
                continue
            if username != "back":
                while True:
                    password = input(
                        "\nPlease enter a password. Enter 'back' to go to the username page.\n"
                    )
                    if password == "back":
                        break
                    if password == "":
                        continue
                    if password != "back":
                        if (self.loginAccount(username, password) == True):
                            self.onLoginPage = False
                            return username

                        

    def create(self):
        self.onCreatePage = True
        while self.onCreatePage:
            username = input("\nPlease enter a username. Enter 'back' to go to the account page.\n")
            if username == "back":
                self.onCreatePage = False
                return
            if username == "":
                continue
            if username != "back":
                if (self.checkUsername(username) == False):
                    while True:
                        password = input(
                            "\nPlease enter a password. (At least 8 chars, 1 number, 1 symbol.) Enter 'back' to go to the username page.\n"
                        )
                        if password == "back":
                            break
                        if len(password) >= 8 and any(char.isdigit() for char in password) and any(not c.isalnum() for c in password):
                            self.addAccountToTable(username, password)
                            self.onCreatePage = False
                            return
                        else:
                            print("Password must be at least 8 characters, 1 number, 1 symbol.")

    def addAccountToTable(self, username, password):
        connection = self.connectDatabase()
        if connection is None:
            print("Database not connected. Cannot add account.")
            return
        
        cursor = connection.cursor()

        insert_query = "INSERT INTO accounts (username, password, is_staff) VALUES (%s, %s, %s)"
        try:
            cursor.execute(insert_query, (username, password, False))
            connection.commit()
            print("Account successfully created. (is_staff = False)")
        except mysql.connector.Error as err:
            print(f"Failed to insert: {err}")
        finally:
            cursor.close()
            connection.close()

    def checkUsername(self, username):
        connection = self.connectDatabase()
        if connection is None:
            print("Database not connected. Cannot add account.")
            return
        
        cursor = connection.cursor()

        select_query = "SELECT * FROM accounts WHERE username = %s"

        try:
            cursor.execute(select_query, (username,))
            result = cursor.fetchone()
            
            if result:
                print("Account already exists.")
                return True
            else:
                print("Account does not exist yet.")
                return False

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return False
        
        finally:
            cursor.close()
            connection.close()

    def loginAccount(self, username, password):
        connection = self.connectDatabase()
        if connection is None:
            print("Database not connected. Cannot add account.")
            return
        
        cursor = connection.cursor()

        select_query = "SELECT * FROM accounts WHERE username = %s AND password = %s"

        try:
            cursor.execute(select_query, (username, password))
            result = cursor.fetchone()
            
            if result:
                print("Login successful.")
                return True
            else:
                print("Incorrect username or password.")
                return False

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return False
        
        finally:
            cursor.close()
            connection.close()
        
    def createAccountsTable(self):
        connection = self.connectDatabase()
        if connection is None:
            print("Database not connected. Cannot create table.")
            return
        
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            is_staff BOOLEAN NOT NULL
        );
        """
        try:
            cursor.execute(create_table_query)
            connection.commit()
            print("'accounts' table is ready (created if it didn't already exist).")
        except mysql.connector.Error as err:
            print(f"Failed to create table: {err}")
        finally:
            cursor.close()
            connection.close()

    def connectDatabase(self):
        try:
            connection = mysql.connector.connect(
                host=self.dbHost,
                user=self.dbUser,
                password=self.dbPwd,
                database=self.dbSqlDb
            )
            print("\nConnected to database successfully.\n")
            return connection
        except mysql.connector.Error as err:
            print(f"\nDatabase connection failed: {err}\n")
            return None


    def accountPage(self):
        self.onAccountPage = True
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "db_creds.txt")
        
        try:
            with open(file_path, "r") as settingsFile:
                for line in settingsFile:
                    splitLine = line.strip().split("=")
                    if (splitLine[0] == "host"):
                        self.dbHost = splitLine[1]
                    if (splitLine[0] == "user"):
                        self.dbUser = splitLine[1]
                    if (splitLine[0] == "pwd"):
                        self.dbPwd = splitLine[1]
                    if (splitLine[0] == "sql_db"):
                        self.dbSqlDb = splitLine[1]   
        except FileNotFoundError:
            print(f"\nError: Could not locate database settings.\n")

        print("\nGot database credentials.\n")

        self.createAccountsTable()

        while self.onAccountPage:
            mode = input(
                "\nWould you like to log into an existing account, or create a new account? (login, create) Enter 'q' to quit.\n"
            )
            if mode == "q":
                break
            elif mode == "login":
                login_username = self.login()
                if login_username:
                    print(f"You are now logged in as: {login_username}")
                    return login_username
            elif mode == "create":
                self.create()
            else:
                print("Please enter a valid option.")