import os
import mysql.connector
import mysql
from payment import Payment
from invoice import Invoice
from db.connect_database import getDatabase

class ShoppingCart:
    def __init__(self):
        self.onShoppingCartPage = True
        self.itemArray = []
        self.quantityArray = []
        self.priceArray = []

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
        
    def getProductName(self, productID):
        connection = self.connectDatabase()
        if connection is None:
            print("\nDatabase not connected. Cannot get product price.\n")
            return None

        cursor = connection.cursor()

        select_query = "SELECT name FROM products WHERE id = %s"

        try:
            cursor.execute(select_query, (productID,))
            result = cursor.fetchone()

            if result:
                name = result[0]
                print(f"\nName for product ID {productID} is: {name}\n")
                return name
            else:
                print(f"\nNo product found with ID {productID}.\n")
                return None

        except mysql.connector.Error as err:
            print(f"\nDatabase error: {err}\n")
            return None

        finally:
            cursor.close()
            connection.close()
        

    def getProductPrice(self, productID):
        connection = self.connectDatabase()
        if connection is None:
            print("\nDatabase not connected. Cannot get product price.\n")
            return None

        cursor = connection.cursor()

        select_query = "SELECT price FROM products WHERE id = %s"

        try:
            cursor.execute(select_query, (productID,))
            result = cursor.fetchone()

            if result:
                price = result[0]
                print(f"\nPrice for product ID {productID} is: {price}\n")
                return price
            else:
                print(f"\nNo product found with ID {productID}.\n")
                return None

        except mysql.connector.Error as err:
            print(f"\nDatabase error: {err}\n")
            return None

        finally:
            cursor.close()
            connection.close()

    def addToCart(self, productID, quantity):
        self.itemArray.append(self.getProductName(productID))
        self.quantityArray.append(quantity)
        self.priceArray.append(self.getProductPrice(productID))

    def checkout(self, username):
        while self.onShoppingCartPage:
            print("\nYour shopping cart contains these items:")
            for i in range(len(self.itemArray)):
                print(self.itemArray[i] + " " + str(self.quantityArray[i]) + "x" + " (Total: $" + str(round((self.quantityArray[i] * self.priceArray[i]), 2)) + ")")
            mode = input(
                "\nWould you like to checkout? ('checkout') Enter 'q' to quit.\n"
            )
            if mode == "q":
                break
            elif mode == "checkout":
                if (username != ""):
                    pay = Payment()
                    payment_details = pay.payment(username)
                    if payment_details:
                        invoice = Invoice()
                        invoice.createInvoice(payment_details, self.itemArray, self.quantityArray, self.priceArray)
                        self.onShoppingCartPage = False
                        return
                else:
                    print("\nYou must be logged in to access the payment gateway!\n")
            else:
                print("Please enter a valid option.")