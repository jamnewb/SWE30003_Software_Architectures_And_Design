import os
import mysql.connector
import mysql
import re

class Payment:
    def __init__(self):
        self.onPaymentPage = False
        self.onSecurityPage = False
        self.dbHost = ""
        self.dbUser = ""
        self.dbPwd = ""
        self.dbSqlDb = ""

    def checkPaymentDetails(self, username):
        connection = self.connectDatabase()
        if connection is None:
            print("\nDatabase not connected. Cannot add account.\n")
            return
        
        cursor = connection.cursor()

        select_query = "SELECT * FROM payment WHERE username = %s"

        try:
            cursor.execute(select_query, (username,))
            result = cursor.fetchone()
            
            if result:
                print("\nPayment details already recorded for this account.\n")
                return True
            else:
                print("\nPayment details are not recorded for this account.\n")
                return False

        except mysql.connector.Error as err:
            print(f"\nDatabase error: {err}\n")
            return False
        
        finally:
            cursor.close()
            connection.close()

    def addPaymentDetails(self, username, first_name, last_name, email, address, phone_number, card_number, card_expiry, card_name):
        connection = self.connectDatabase()
        if connection is None:
            print("\nDatabase not connected. Cannot add payment details.\n")
            return
        
        cursor = connection.cursor()
        
        cursor = connection.cursor()

        insert_query = "INSERT INTO payment (username, first_name, last_name, email, address, phone_number, card_number, card_expiry, card_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(insert_query, (username, first_name, last_name, email, address, phone_number, card_number, card_expiry, card_name))
            connection.commit()
            print("\nPayment details successfully added\n")
        except mysql.connector.Error as err:
            print(f"\nFailed to insert: {err}\n")
        finally:
            cursor.close()
            connection.close()

    def deleteRecord(self, username):
        connection = self.connectDatabase()
        if connection is None:
            print("\nDatabase not connected. Cannot delete payment details.\n")
            return
        
        cursor = connection.cursor()

        delete_query = "DELETE FROM payment WHERE username = %s"
        
        try:
            cursor.execute(delete_query, (username,))
            connection.commit()
            if cursor.rowcount > 0:
                print("\nPayment details successfully deleted.\n")
            else:
                print("\nNo payment record found for that username.\n")

        except mysql.connector.Error as err:
            print(f"\nFailed to delete: {err}\n")
        finally:
            cursor.close()
            connection.close()

    def getPaymentDetails(self, username):
        connection = self.connectDatabase()
        if connection is None:
            print("\nDatabase not connected. Cannot get payment details.\n")
            return None
        
        cursor = connection.cursor()

        select_query = """
            SELECT first_name, last_name, email, address, phone_number,
                card_number, card_expiry, card_name
            FROM payment
            WHERE username = %s
        """

        try:
            cursor.execute(select_query, (username,))
            result = cursor.fetchone()

            if result:
                print("\nPayment details found.\n")
                (first_name, last_name, email, address, phone_number,
                card_number, card_expiry, card_name) = result

                return {
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "address": address,
                    "phone_number": phone_number,
                    "card_number": card_number,
                    "card_expiry": card_expiry,
                    "card_name": card_name
                }
            else:
                print("\nNo payment record found for this username.\n")
                return None

        except mysql.connector.Error as err:
            print(f"\nDatabase error: {err}\n")
            return None
        
        finally:
            cursor.close()
            connection.close()

    def sendPaymentDetails(self, first_name, last_name, email, address, phone_number, card_number, card_security, card_name, card_expiry):
        print("\nSent the details to the third party payment gateway!\n")
        print("\nDetails sent:\n"
              + first_name + "\n"
              + last_name + "\n"
              + email + "\n"
              + address + "\n"
              + phone_number + "\n"
              + card_number + "\n"
              + card_security + "\n"
              + card_name + "\n"
              + card_expiry + "\n")

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
        
    def createPaymentTable(self):
        connection = self.connectDatabase()
        if connection is None:
            print("\nDatabase not connected. Cannot create table.\n")
            return
        
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS payment (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL,
            phone_number VARCHAR(10) NOT NULL,
            card_number VARCHAR(16) NOT NULL,
            card_expiry VARCHAR(5) NOT NULL,
            card_name VARCHAR(255) NOT NULL
        );
        """
        try:
            cursor.execute(create_table_query)
            connection.commit()
            print("\n'payment' table is ready (created if it didn't already exist).\n")
        except mysql.connector.Error as err:
            print(f"\nFailed to create table: {err}\n")
        finally:
            cursor.close()
            connection.close()

    def security_input(self, username, first_name, last_name, email, address, phone_number, card_number, card_expiry, card_name):
        self.onSecurityPage = True
        while self.onSecurityPage:
            card_security = input(
            "\nPlease enter your card's 3 digit security number. Enter 'back' to go back to the main menu.\n"
            )
            if card_security == "back":
                self.onSecurityPage = False
                return
            if card_security == "":
                continue
            if card_security != "back":
                if (card_security.isnumeric() and len(card_security) == 3):
                    if (self.checkPaymentDetails(username) == False):
                        self.addPaymentDetails(username, first_name, last_name, email, address, phone_number, card_number, card_expiry, card_name)
                        self.sendPaymentDetails(first_name, last_name, email, address, phone_number, card_number, card_expiry, card_name, card_security)
                        self.onSecurityPage = False
                        return {
                            "username": username,
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "address": address,
                            "phone_number": phone_number,
                            "card_number": card_number,
                            "card_security": card_expiry,
                            "card_name": card_name,
                            "card_expiry": card_security
                        }
                    else:
                        self.sendPaymentDetails(first_name, last_name, email, address, phone_number, card_number, card_expiry, card_name, card_security)
                        self.onSecurityPage = False
                        return {
                            "username": username,
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "address": address,
                            "phone_number": phone_number,
                            "card_number": card_number,
                            "card_security": card_expiry,
                            "card_name": card_name,
                            "card_expiry": card_security
                        }
                else:
                    print("\nSecurity number must be a 3 digit number.\n")



    def payment(self, username):
        self.onPaymentPage = True

        #paymentLocations = ["first_name", "last_name", "email", "address", "phone_number", "card_number", "card_security", "card_name", "card_expiry"]

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

        self.createPaymentTable()

        if (self.checkPaymentDetails(username) == False):
            while self.onPaymentPage:
                first_name = input(
                    "\nPlease enter your first name. Enter 'back' to go back to the main menu.\n"
                )
                if first_name == "back":
                    break
                if first_name == "":
                    continue
                if first_name != "back":
                    if (first_name.isalpha()):
                        while (True):
                            last_name = input(
                                "\nPlease enter your last name. Enter 'back' to go back to the main menu.\n"
                            )
                            if last_name == "back":
                                break
                            if last_name == "":
                                continue
                            if last_name != "back":
                                if (last_name.isalpha()):
                                    while (True):
                                        email = input(
                                            "\nPlease enter your email. Enter 'back' to go back to the main menu.\n"
                                        )
                                        if email == "back":
                                            break
                                        if email == "":
                                            continue
                                        if email != "back":
                                            if ("@" in email and "." in email and len(email) >= 4):
                                                while (True):
                                                    address = input(
                                                        "\nPlease enter your address. Enter 'back' to go back to the main menu.\n"
                                                    )
                                                    if address == "back":
                                                        break
                                                    if address == "":
                                                        continue
                                                    if address != "back":
                                                        split_address = address.split(" ", 1)
                                                        if (" " in address):
                                                            if (split_address[0].isnumeric() and re.fullmatch(r"[A-Za-z ]+", split_address[1])):
                                                                while (True):
                                                                    phone_number = input(
                                                                        "\nPlease enter your phone number. Enter 'back' to go back to the main menu.\n"
                                                                    )
                                                                    if phone_number == "back":
                                                                        break
                                                                    if phone_number == "":
                                                                        continue
                                                                    if phone_number != "back":
                                                                        if (phone_number.isnumeric() and phone_number[0] == "0" and len(phone_number) == 10):
                                                                            while (True):
                                                                                card_number = input(
                                                                                    "\nPlease enter your card number. Enter 'back' to go back to the main menu.\n"
                                                                                )
                                                                                if card_number == "back":
                                                                                    break
                                                                                if card_number == "":
                                                                                    continue
                                                                                if card_number != "back":
                                                                                    if (card_number.isnumeric() and len(card_number) == 16):
                                                                                        while (True):
                                                                                            card_expiry = input(
                                                                                                "\nPlease enter the expiry date of your card. Enter 'back' to go back to the main menu.\n"
                                                                                            )
                                                                                            if card_expiry == "back":
                                                                                                break
                                                                                            if card_expiry == "":
                                                                                                continue
                                                                                            if card_expiry != "back":
                                                                                                if ("/" in card_expiry):
                                                                                                    split_card_expiry = card_expiry.split("/", 1)
                                                                                                    print(split_card_expiry[0])
                                                                                                    if (split_card_expiry[0].isnumeric() and len(split_card_expiry[0])==2 and 
                                                                                                        split_card_expiry[1].isnumeric() and len(split_card_expiry[1])==2):
                                                                                                            while (True):
                                                                                                                card_name = input(
                                                                                                                    "\nPlease enter the name on your card. Enter 'back' to go back to the main menu.\n"
                                                                                                                )
                                                                                                                if card_name == "back":
                                                                                                                    break
                                                                                                                if card_name == "":
                                                                                                                    continue
                                                                                                                if card_name != "back":
                                                                                                                    if (re.fullmatch(r"[A-Za-z ]+", card_name)):
                                                                                                                        payment_data = self.security_input(username, first_name, last_name, email, address, phone_number, card_number, card_expiry, card_name)
                                                                                                                        if payment_data:
                                                                                                                            self.onPaymentPage = False
                                                                                                                            return payment_data
                                                                                                                    else:
                                                                                                                        print("\nCard name must only include letters and spaces.\n")                 
                                                                                                    else:
                                                                                                        print("\nExpiration date must be of the format 'xx/xx' where 2 two digit numbers are broken up by a slash.\n")
                                                                                                else:
                                                                                                    print("\nExpiration date must be of the format 'xx/xx' where 2 two digit numbers are broken up by a slash.\n")
                                                                                    else:
                                                                                        print("\nCard number must be a 16 digit number.\n")
                                                                        else:
                                                                            print("\nPhone number must begin with a '0' and be a 16 digit number in total.\n")
                                                            else:
                                                                print("\nAddress must be of the format '[street number] [street name]'.\n")
                                                        else:
                                                            print("\nAddress must be of the format '[street number] [street name]'.\n")
                                                                                                                                    
                                            else:
                                                print("\nEmail must contain some characters broken up by a '@' and a '.'\n")
                                else:
                                    print("\nLast name must only contain letters.\n")
                                        
                    else:
                        print("\nFirst name must only contain letters.\n")
        else:
            while (True):
                mode = input(
                    "\nPayment details have already been recorded for this account.\nIf you would like to use these details to pay, type 'use', if you would like to delete this record, type 'delete'.\nIf you would like to go back to the main menu, type 'back'.\n"
                )
                if mode == "back":
                    break
                if mode == "":
                    continue
                if mode == "delete":
                    self.deleteRecord(username)
                    return
                if mode == "use":
                    result = self.getPaymentDetails(username)

                    if result is not None:
                        payment_info = self.security_input(
                            result["username"],
                            result["first_name"],
                            result["last_name"],
                            result["email"],
                            result["address"],
                            result["phone_number"],
                            result["card_number"],
                            result["card_expiry"],
                            result["card_name"]
                        )
                        if payment_info:
                            self.onPaymentPage = False
                            return payment_info