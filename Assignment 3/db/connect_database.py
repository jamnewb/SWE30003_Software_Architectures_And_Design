import mysql.connector
import mysql    

def connectDatabase(dbHost, dbUser, dbPwd, sqlDB):
    """
    Initialises a DB object which interfaces with MySQL
    """

    # Establish a MySQL connection using the credentials stored locally
    try:
        connection = mysql.connector.connect(
            host=dbHost,
            user=dbUser,
            password=dbPwd,
            database=sqlDB
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection failed: {err}")

def getDatabaseCreds(path): 
    """
    Gets the database credentials we need to initialise a connection with MySQL
    """

    try:
        # Read through the credentials file and store all of the values
        with open(path, "r") as settingsFile:
            for line in settingsFile:
                splitLine = line.strip().split("=")
                if (splitLine[0] == "host"):
                    dbHost = splitLine[1]
                if (splitLine[0] == "user"):
                    dbUser = splitLine[1]
                if (splitLine[0] == "pwd"):
                    dbPwd = splitLine[1]
                if (splitLine[0] == "sql_db"):
                    dbSqlDb = splitLine[1]   
    except FileNotFoundError:
        print(f"Error: Could not locate database settings.")

    # Return them
    return dbHost, dbUser, dbPwd, dbSqlDb

def getDatabase():

    # Get the database information from SQL using the credentials
    host, user, pwd, sqlDB = getDatabaseCreds("db_creds.txt")
    # Use this information to init a database object we can use across the application
    dbConnection = connectDatabase(host, user, pwd, sqlDB)

    # Return it
    return dbConnection