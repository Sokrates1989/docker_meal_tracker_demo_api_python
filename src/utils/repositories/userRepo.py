### Wraps all direct interaction with user part of DB.


class UserRepo:

    # Constructor.
    def __init__(self, dbAnandaTrackerWrapper):
        self.dbWrapper = dbAnandaTrackerWrapper

    # Validate user password.
    # Pass credentialsItem.
    def isUserPasswordCorrect(self, credentialsItem):

        if self.dbWrapper.isTokenValid(credentialsItem.token) == False:
            print("invalid token")
            return False
        else:
            # Does user already exist?
            user = self.getUserByName(credentialsItem.userName)
            if user is None:
                return None
            else:
                if user["hashedPassword"] == credentialsItem.hashedPassword:
                    return True
                else:
                    return "invalid password"
                    

    # Get user by its ID.
    # Pass user ID as parameter.
    # Return is an associative array or None.
    def getUserByID(self, userID, alreadyAttemptedToUpdateOwnClassVars=False):

        try:
            query = "SELECT " \
                    "ID, " \
                    "AES_DECRYPT(name_encr, '" + str(self.dbWrapper.encryptionKey) + "') as name, " \
                    "hashedPassword " \
                    "FROM users WHERE ID=%s "
            val = (userID,)
            self.dbWrapper.dbCursor.execute(query, val)
            myresult = self.dbWrapper.dbCursor.fetchone()

            # Did query retrieve valid user?
            user = None
            if (myresult != None):
                user = {
                    'ID': myresult[0],
                    'name': '' if myresult[1] is None else myresult[1].decode(),
                    'hashedPassword': myresult[2],
                }
            return user

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            else:
                # Make sure, that own class vars are valid.
                self.dbWrapper.updateOwnClassVars()
                return self.dbWrapper.getUserRepo().getUserByID(userID, True)

    # Get user by its name.
    # Pass user ID as parameter.
    # Return is an associative array or None.
    def getUserByName(self, userName, alreadyAttemptedToUpdateOwnClassVars=False):

        try:
            query = "SELECT ID FROM users WHERE AES_DECRYPT(name_encr, '" + \
                    str(self.dbWrapper.encryptionKey) + "') = %s "
            val = (userName,)
            self.dbWrapper.dbCursor.execute(query, val)
            myresult = self.dbWrapper.dbCursor.fetchone()

            # Did query retrieve valid user?
            user = None
            if (myresult != None and myresult != None):
                user = self.getUserByID(myresult[0])
            return user

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            else:
                # Make sure, that own class vars are valid.
                self.dbWrapper.updateOwnClassVars()
                return self.dbWrapper.getUserRepo().getUserByName(userName, True)


    # Get user by credentialsItem.
    # Pass credentialsItem as parameter.
    # Return is an associative array or None.
    def getUserByCredentialsItem(self, credentialsItem):
        return self.getUserByName(credentialsItem.userName)

    # Get user ID by credentialsItem.
    # Pass credentialsItem as parameter.
    # Return is ID or None.
    def getUserIDByCredentialsItem(self, credentialsItem):
        user = self.getUserByName(credentialsItem.userName)
        userID = user["ID"]
        return userID

    # Get all user IDs
    def getAllUserIDs(self, alreadyAttemptedToUpdateOwnClassVars=False):

        try:
            query = "SELECT ID FROM users"
            self.dbWrapper.dbCursor.execute(query)
            myresults = self.dbWrapper.dbCursor.fetchall()

            # Did query retrieve users?
            userIDs = []
            if (myresults != None):
                for result in myresults:
                    userIDs.append(result[0])
            return userIDs

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            else:
                # Make sure, that own class vars are valid.
                self.dbWrapper.updateOwnClassVars()
                return self.dbWrapper.getUserRepo().getAllUserIDs(True)

    # Create new user.
    # return newly created user ID.
    def createNewUser(self, name, hashedPassword, alreadyAttemptedToUpdateOwnClassVars=False):

        try:
            # Does User already exist?
            user = self.getUserByName(name)
            if (user == None):

                # Prepare insert sql string.
                sql = "INSERT INTO users (name_encr, hashedPassword) VALUES (" \
                    "AES_ENCRYPT(%s, '" + str(self.dbWrapper.encryptionKey) + "'), " \
                    "%s " \
                    ")"
                val = (name, hashedPassword)

                # Execute insert query.
                self.dbWrapper.dbCursor.execute(sql, val)
                self.dbWrapper.dbConnection.commit()

                return self.getUserByID(self.dbWrapper.dbCursor.lastrowid)
            else:
                # Return None to indicate, that user already exists.
                return None

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            else:
                # Make sure, that own class vars are valid.
                self.dbWrapper.updateOwnClassVars()
                return self.dbWrapper.getUserRepo().createNewUser(name, hashedPassword, True)

    # Create new user.
    # return newly created user ID.
    def createNewUser_fromCredentialsItem(self, credentialsItem):
        return self.createNewUser(credentialsItem.userName, credentialsItem.hashedPassword)
            
