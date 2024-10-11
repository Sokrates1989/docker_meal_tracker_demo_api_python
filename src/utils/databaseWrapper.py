### Class for any interaction with the DB.
### All write and read operations of DB should be done in this file/ class.
### Uses repositories to separate logical components.

## Imports.
# database connection.
import mysql.connector
# For getting config.
import json
# To retrieve current timestamp.
import time

# Import own classes.
# Insert path to own stuff to allow importing them.
import os
import sys

sys.path.insert(1, os.path.join(os.path.dirname(__file__), "..", "utils"))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "..", "models"))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "repositories"))

# Repositories containing logical parts.
import userRepo as UserRepo

# CredentialsItem from own models to use location independent.
import credentialsItem as CredentialsItem


class DatabaseWrapper:

    # Constructor.
    def __init__(self):

        # Get credentials for database from config file.
        config_file_pathAndName = os.path.join(os.path.dirname(__file__), "..", "..", "config.txt")
        config_file = open(config_file_pathAndName)
        config_array = json.load(config_file)

        # Database connection
        self.dbConnection = mysql.connector.connect(
            host=config_array["database"]["host"],
            user=config_array["database"]["user"],
            password=config_array["database"]["password"],
            database=config_array["database"]["database"],
            port=config_array["database"]["port"]
        )
        self.dbCursor = self.dbConnection.cursor(
            buffered=True)  # need to buffer to fix mysql.connector.errors.InternalError: Unread result found (https://stackoverflow.com/questions/29772337/python-mysql-connector-unread-result-found-when-using-fetchone)
        self.validToken = config_array["authentication"]["token"]
        self.encryptionKey = config_array["authentication"]["encryption_key"]


    def updateOwnClassVars(self):

        # Get credentials for database from config file.
        config_file_pathAndName = os.path.join(os.path.dirname(__file__), "..", "..", "config.txt")
        config_file = open(config_file_pathAndName)
        config_array = json.load(config_file)

        # Database connection
        self.dbConnection = mysql.connector.connect(
            host=config_array["database"]["host"],
            user=config_array["database"]["user"],
            password=config_array["database"]["password"],
            database=config_array["database"]["database"],
            port=config_array["database"]["port"]
        )
        self.dbCursor = self.dbConnection.cursor(
            buffered=True)  # need to buffer to fix mysql.connector.errors.InternalError: Unread result found (https://stackoverflow.com/questions/29772337/python-mysql-connector-unread-result-found-when-using-fetchone)

        # "Log" info.
        print("Database: Updated own class vars")


    def getUserRepo(self):
        return UserRepo.UserRepo(self)


    # Determine if authentication is valid.
    def isTokenValid(self, token):
        if token == self.validToken:
            return True
        else:
            return False

