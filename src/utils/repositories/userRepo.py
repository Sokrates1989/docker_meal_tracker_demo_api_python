# Copyright (C) 2024 Patrick Michiels
# All rights reserved.
# This source code is licensed under the Evaluation License Agreement and
# may not be used, modified, or distributed without explicit permission from the author.
# This code is provided for evaluation purposes only.

class UserRepo:
    """
    Repository class for managing user-related interactions with the database.

    This class wraps direct interaction with the user part of the database, including validating user credentials,
    retrieving user data by ID or name, and creating new users.
    
    Attributes:
        dbWrapper: The database wrapper that provides database connection and cursor.
    """

    def __init__(self, dbAnandaTrackerWrapper):
        """
        Initializes the UserRepo with a database wrapper.

        Args:
            dbAnandaTrackerWrapper: The database wrapper object used to interact with the database.
        """
        self.dbWrapper = dbAnandaTrackerWrapper

    def isUserPasswordCorrect(self, credentialsItem) -> bool or str or None:
        """
        Validates the user's password.

        Args:
            credentialsItem: The credentialsItem object containing the user's token, username, and hashed password.

        Returns:
            bool or str or None: 
                - True if the password is correct,
                - "invalid password" if the password is incorrect,
                - False if the token is invalid,
                - None if the user does not exist.
        """
        if not self.dbWrapper.isTokenValid(credentialsItem.token):
            print("invalid token")
            return False

        user = self.getUserByName(credentialsItem.userName)
        if user is None:
            return None
        if user["hashedPassword"] == credentialsItem.hashedPassword:
            return True
        return "invalid password"

    def getUserByID(self, userID: int, alreadyAttemptedToUpdateOwnClassVars: bool = False) -> dict or None:
        """
        Retrieves a user by their ID from the database.

        Args:
            userID (int): The ID of the user.
            alreadyAttemptedToUpdateOwnClassVars (bool): Flag to prevent multiple updates in case of error.

        Returns:
            dict or None: A dictionary containing the user details if found, otherwise None.
        """
        try:
            query = """
                SELECT ID, 
                       AES_DECRYPT(name_encr, %s) as name, 
                       hashedPassword 
                FROM users 
                WHERE ID=%s
            """
            val = (str(self.dbWrapper.encryptionKey), userID)
            self.dbWrapper.dbCursor.execute(query, val)
            myresult = self.dbWrapper.dbCursor.fetchone()

            if myresult:
                return {
                    'ID': myresult[0],
                    'name': '' if myresult[1] is None else myresult[1].decode(),
                    'hashedPassword': myresult[2],
                }
            return None

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            self.dbWrapper.updateOwnClassVars()
            return self.dbWrapper.getUserRepo().getUserByID(userID, True)

    def getUserByName(self, userName: str, alreadyAttemptedToUpdateOwnClassVars: bool = False) -> dict or None:
        """
        Retrieves a user by their name from the database.

        Args:
            userName (str): The name of the user.
            alreadyAttemptedToUpdateOwnClassVars (bool): Flag to prevent multiple updates in case of error.

        Returns:
            dict or None: A dictionary containing the user details if found, otherwise None.
        """
        try:
            query = """
                SELECT ID 
                FROM users 
                WHERE AES_DECRYPT(name_encr, %s) = %s
            """
            val = (str(self.dbWrapper.encryptionKey), userName)
            self.dbWrapper.dbCursor.execute(query, val)
            myresult = self.dbWrapper.dbCursor.fetchone()

            if myresult:
                return self.getUserByID(myresult[0])
            return None

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            self.dbWrapper.updateOwnClassVars()
            return self.dbWrapper.getUserRepo().getUserByName(userName, True)

    def getUserByCredentialsItem(self, credentialsItem) -> dict or None:
        """
        Retrieves a user by their credentials.

        Args:
            credentialsItem: The credentialsItem object containing the user's token, username, and hashed password.

        Returns:
            dict or None: A dictionary containing the user details if found, otherwise None.
        """
        return self.getUserByName(credentialsItem.userName)

    def getUserIDByCredentialsItem(self, credentialsItem) -> int or None:
        """
        Retrieves the user ID by their credentials.

        Args:
            credentialsItem: The credentialsItem object containing the user's token, username, and hashed password.

        Returns:
            int or None: The user ID if found, otherwise None.
        """
        user = self.getUserByName(credentialsItem.userName)
        return user["ID"] if user else None

    def getAllUserIDs(self, alreadyAttemptedToUpdateOwnClassVars: bool = False) -> list or None:
        """
        Retrieves all user IDs from the database.

        Args:
            alreadyAttemptedToUpdateOwnClassVars (bool): Flag to prevent multiple updates in case of error.

        Returns:
            list or None: A list of user IDs if found, otherwise None.
        """
        try:
            query = "SELECT ID FROM users"
            self.dbWrapper.dbCursor.execute(query)
            myresults = self.dbWrapper.dbCursor.fetchall()

            return [result[0] for result in myresults] if myresults else []

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            self.dbWrapper.updateOwnClassVars()
            return self.dbWrapper.getUserRepo().getAllUserIDs(True)

    def createNewUser(self, name: str, hashedPassword: str, alreadyAttemptedToUpdateOwnClassVars: bool = False) -> dict or None:
        """
        Creates a new user in the database.

        Args:
            name (str): The name of the user.
            hashedPassword (str): The hashed password of the user.
            alreadyAttemptedToUpdateOwnClassVars (bool): Flag to prevent multiple updates in case of error.

        Returns:
            dict or None: A dictionary containing the newly created user details, or None if the user already exists.
        """
        try:
            user = self.getUserByName(name)
            if user is None:
                query = """
                    INSERT INTO users (name_encr, hashedPassword) 
                    VALUES (AES_ENCRYPT(%s, %s), %s)
                """
                val = (name, str(self.dbWrapper.encryptionKey), hashedPassword)
                self.dbWrapper.dbCursor.execute(query, val)
                self.dbWrapper.dbConnection.commit()

                return self.getUserByID(self.dbWrapper.dbCursor.lastrowid)
            return None

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            self.dbWrapper.updateOwnClassVars()
            return self.dbWrapper.getUserRepo().createNewUser(name, hashedPassword, True)

    def createNewUser_fromCredentialsItem(self, credentialsItem) -> dict or None:
        """
        Creates a new user in the database from a credentialsItem object.

        Args:
            credentialsItem: The credentialsItem object containing the user's token, username, and hashed password.

        Returns:
            dict or None: A dictionary containing the newly created user details, or None if the user already exists.
        """
        return self.createNewUser(credentialsItem.userName, credentialsItem.hashedPassword)
