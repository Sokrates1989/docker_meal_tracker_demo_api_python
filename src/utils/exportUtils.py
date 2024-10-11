## Utilities for exporting database.

# Get Config.
import os
import json

# For threading to not block main thread.
from multiprocessing import Process
import multiprocessing

# Database Connection.
import databaseWrapper as DatabaseWrapper

# Logger.
import logger as Logger
from src.models.credentialsItem import CredentialsItem


class ExportUtils:

    # Constructor creating logfiles and paths.
    def __init__(self):

        # Get credentials for database from config file.
        config_file_pathAndName = os.path.join(os.path.dirname(__file__), "..", "..", "config.txt")
        config_file = open(config_file_pathAndName)
        config_array = json.load(config_file)

        # TimeoutDuration for multiprocessing.
        self.timeoutDuration = config_array["export"]["timeoutDuration"]

        # Prepare Logger.
        self.logger = Logger.Logger()

        # Get database connection.
        self.dbWrapper = DatabaseWrapper.DatabaseWrapper()

        # To retrieve return from process.
        # Preventing OSError: [Errno 98] Address in use.
        try:
            self.manager = multiprocessing.Manager()
        except Exception as e:
            print("could not start multiprocessing")

    def updateOwnClassVars(self):

        # Prepare Logger.
        self.logger = Logger.Logger()

        # Get database connection.
        self.dbWrapper = DatabaseWrapper.DatabaseWrapper()

        # To retrieve return from process.
        # Preventing OSError: [Errno 98] Address in use.
        try:
            self.manager = multiprocessing.Manager()
        except Exception as e:
            print("could not start multiprocessing")

        # "Log" info.
        print("ExportUtils: Updated own class vars")

    # Get json string of current database version for user asynchronously.
    def getDatabaseAsJson(self, credentialsItem: CredentialsItem):

        # Pass return via parameter, since we are using multiprocessing.
        if not self.manager:
            self.manager = multiprocessing.Manager()
        return_dict = self.manager.dict()

        p1 = Process(target=self.addDatabaseAsJsonToReturnDict,
                     args=(credentialsItem, return_dict), name='addDatabaseAsJsonToReturnDict')
        p1.start()
        p1.join(timeout=int(self.timeoutDuration))
        p1.terminate()

        # Log any exitCode, that is not 0 (successful exit of process)
        if (p1.exitcode == None):
            logMessage = "exportUtils.py: addDatabaseAsJsonToReturnDictProcess: operation took more than " + str(
                self.timeoutDuration) + " seconds. Aborted."
            print(logMessage)
            self.logger.logError(logMessage)
            return_dict["returnState"] = "TimeOut"
            return_dict["exitCode"] = "None"

        else:
            if (p1.exitcode != 0):
                logMessage = "exportUtils.py: getDatabaseAsJson: The process returned an unnatural exitcode: " + str(
                    p1.exitcode)
                print(logMessage)
                self.logger.logError(logMessage)
                return_dict["returnState"] = "ExitError"
                return_dict["exitCode"] = p1.exitcode

        return return_dict

    # Get json string of current database version for user.
    def addDatabaseAsJsonToReturnDict(self, credentialsItem: CredentialsItem, return_dict):

        if self.dbWrapper.isUserPasswordCorrect(credentialsItem) == True:

            databaseAsDict = {
                "tasks": self.dbWrapper.getAllTasks(credentialsItem),
                "user": self.dbWrapper.getUserByName(credentialsItem.token, credentialsItem.userName),
            }

            return_dict["returnState"] = "Success"
            return_dict["databaseAsJson"] = databaseAsDict

        else:
            return_dict["returnState"] = "Invalid Credentials"

        return return_dict
