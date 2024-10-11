### Class for any interaction with the DB.
### All write and read operations of DB should be done in this file/ class.
### This class contains many functions from an older project => you can 
### delete them, but they might serve you as a good reference how to create a 
### databaseWrapper.

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

# CredentialsItem from own models to use location independent.
import credentialsItem as CredentialsItem


class DatabaseWrapper:

    # Constructor.
    def __init__(self):

        self.updateOwnClassVars()

    def updateOwnClassVars(self):
        # Get credentials for database from config file.
        config_file_pathAndName = os.path.join(os.path.dirname(__file__), "..", "..", "config.txt")
        config_file = open(config_file_pathAndName)
        config_array = json.load(config_file)

        # Database connection.
        self.mydb = mysql.connector.connect(
            host=config_array["database"]["host"],
            user=config_array["database"]["user"],
            password=config_array["database"]["password"],
            database=config_array["database"]["database"],
            port=config_array["database"]["port"]
        )
        self.myCursor = self.mydb.cursor(
            buffered=True)  # need to buffer to fix mysql.connector.errors.InternalError: Unread result found
        self.validToken = config_array["authentication"]["token"]
        print("Database: Updated own class vars")

    # Determine if authentication is valid.
    def isTokenValid(self, token, alreadyAttemptedToUpdateOwnClassVars=False):
        try:
            if token == self.validToken:
                return True
            else:
                return False
        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                raise e
            else:
                self.updateOwnClassVars()
                return self.isTokenValid(token, True)

    # Get next ID imitating auto increment.
    def getNextID(self, table, userID, alreadyAttemptedToUpdateOwnClassVars=False):
        try:
            idColumnName = "ID"
            userColumnName = "fk_user_id"
            if table == "tasks":
                idColumnName = "ID"
                userColumnName = "fk_user_id"
            elif table == "devices":
                idColumnName = "ID"
                userColumnName = "fk_user_id"
            elif table == "db_versions":
                idColumnName = "db_version"
                userColumnName = "fk_user_id"
            else:
                return 1

            query = "SELECT MAX(" + idColumnName + ") as highestID FROM " + table + " WHERE " + userColumnName + " = %s"
            val = (userID,)
            self.myCursor.execute(query, val)
            myResult = self.myCursor.fetchone()

            # Get the currently highest ID.
            if myResult is not None:
                nextID = 1
                try:
                    nextID = int(myResult[0]) + 1
                except Exception as e:
                    nextID = 1
                return nextID
            else:
                return 1
        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                raise e
            else:
                self.updateOwnClassVars()
                return self.getNextID(self, table, userID, True)


    # Create user.
    # Pass credentialsItem.
    def createUser(self, credentialsItem, alreadyAttemptedToUpdateOwnClassVars=False):
        try:

            if self.isTokenValid(credentialsItem.token) == False:
                print("invalid token")
                return False
            else:
                # Does user already exist?
                credentialsItemReturn = self.getCredentialsItemByName(credentialsItem.token, credentialsItem.userName)
                if credentialsItemReturn is None:
                    # Create new user.
                    # Execute insert query to create a new user.
                    insertSql = "INSERT INTO users (name, hashedPassword) VALUES (%s, %s)"
                    val = (credentialsItem.userName, credentialsItem.hashedPassword)
                    self.myCursor.execute(insertSql, val)

                    # Was query successful? Return -1 if no row was affected.
                    if self.myCursor.rowcount == 0:
                        return -1

                    insertedItemID = self.myCursor.lastrowid
                    self.mydb.commit()

                    # Return newly created user.
                    return self.getUserByID(credentialsItem.token, insertedItemID)
                else:
                    return None
        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                raise e
            else:
                self.updateOwnClassVars()
                return self.createUser(self, credentialsItem, True)

    # Validate user password.
    # Pass credentialsItem.
    def isUserPasswordCorrect(self, credentialsItem, alreadyAttemptedToUpdateOwnClassVars=False):
        try:

            if self.isTokenValid(credentialsItem.token) == False:
                print("invalid token")
                return False
            else:
                # Does user already exist?
                user = self.getUserByName(credentialsItem.token, credentialsItem.userName)
                if user is None:
                    return None
                else:
                    if user["hashedPassword"] == credentialsItem.hashedPassword:
                        return True
                    else:
                        return "invalid password"
        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                raise e
            else:
                self.updateOwnClassVars()
                return self.isUserPasswordCorrect(self, credentialsItem, True)

    # Get CredentialsItem by its name.
    # Pass token and name as parameter.
    # Return is credentialsItem or None.
    def getCredentialsItemByName(self, token, name, alreadyAttemptedToUpdateOwnClassVars=False):
        try:

            if self.isTokenValid(token) == False:
                print("invalid token")
                return False
            else:
                query = "SELECT ID, name, hashedPassword FROM users WHERE name=%s "
                val = (name,)
                self.myCursor.execute(query, val)
                myResult = self.myCursor.fetchone()

                # Did query retrieve valid user?
                credentialsItem = None
                if myResult is not None:
                    credentialsItemHelper = {
                        'ID': myResult[0],
                        'userName': myResult[1],
                        'hashedPassword': myResult[2]
                    }

                    credentialsItem = CredentialsItem.CredentialsItem(
                        token,
                        credentialsItemHelper["userName"],
                        credentialsItemHelper["hashedPassword"]
                    )
                return credentialsItem
        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                raise e
            else:
                self.updateOwnClassVars()
                return self.getCredentialsItemByName(self, token, name, True)

    # Get user by its name.
    # Pass token and name as parameter.
    # Return user or None.
    def getUserByName(self, token, name, alreadyAttemptedToUpdateOwnClassVars=False):
        try:

            if self.isTokenValid(token) == False:
                print("invalid token")
                return False
            else:
                query = "SELECT ID FROM users WHERE name=%s "
                val = (name,)
                self.myCursor.execute(query, val)
                myResult = self.myCursor.fetchone()

                # Did query retrieve valid user?
                user = None
                if myResult is not None:
                    user = self.getUserByID(token, myResult[0])
                return user
        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                raise e
            else:
                self.updateOwnClassVars()
                return self.getUserByName(self, token, name, True)


    # Get user by its ID.
    # Pass token and name as parameter.
    # Return user or None.
    def getUserByID(self, token, userID, alreadyAttemptedToUpdateOwnClassVars=False):
        try:

            if self.isTokenValid(token) == False:
                print("invalid token")
                return False
            else:
                query = "SELECT ID, name, hashedPassword FROM users WHERE ID=%s "
                val = (userID,)
                self.myCursor.execute(query, val)
                myResult = self.myCursor.fetchone()

                # Did query retrieve valid user?
                user = None
                if myResult is not None:
                    user = {
                        'ID': myResult[0],
                        'name': myResult[1],
                        'hashedPassword': myResult[2]
                    }
                return user
        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                raise e
            else:
                self.updateOwnClassVars()
                return self.getUserByID(self, token, userID, True)
