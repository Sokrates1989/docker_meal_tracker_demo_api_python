# Copyright (C) 2024 Patrick Michiels
# All rights reserved.
# This source code is licensed under the Evaluation License Agreement and
# may not be used, modified, or distributed without explicit permission from the author.
# This code is provided for evaluation purposes only.

class DayRepo:
    """
    Repository class for managing day records in the database.

    This class provides methods to retrieve and create day entries based on their IDs or date (year, month, day).
    
    Attributes:
        dbWrapper: The database wrapper that provides database connection and cursor.
    """

    def __init__(self, dbWrapper):
        """
        Initializes the DayRepo with a database wrapper.

        Args:
            dbWrapper: The database wrapper object used to interact with the database.
        """
        self.dbWrapper = dbWrapper

    def getDayByID(self, dayID: int, alreadyAttemptedToUpdateOwnClassVars: bool = False) -> dict or None:
        """
        Retrieves a day entry by its ID from the database.

        Args:
            dayID (int): The ID of the day entry.
            alreadyAttemptedToUpdateOwnClassVars (bool): Flag to prevent multiple updates in case of error.

        Returns:
            dict or None: A dictionary containing the day details if found, otherwise None.
        """
        try:
            query = "SELECT ID, year, month, day FROM days WHERE ID=%s"
            val = (dayID,)
            self.dbWrapper.dbCursor.execute(query, val)
            myresult = self.dbWrapper.dbCursor.fetchone()

            if myresult:
                day = {
                    'ID': myresult[0],
                    'year': myresult[1],
                    'month': myresult[2],
                    'day': myresult[3]
                }
                return day
            return None

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            self.dbWrapper.updateOwnClassVars()
            return self.getDayByID(dayID, True)

    def getDayByDate(self, year: int, month: int, day: int, alreadyAttemptedToUpdateOwnClassVars: bool = False) -> dict or None:
        """
        Retrieves a day entry by its date (year, month, day) from the database.

        Args:
            year (int): The year of the day entry.
            month (int): The month of the day entry.
            day (int): The day of the day entry.
            alreadyAttemptedToUpdateOwnClassVars (bool): Flag to prevent multiple updates in case of error.

        Returns:
            dict or None: A dictionary containing the day details if found, otherwise None.
        """
        try:
            query = "SELECT ID FROM days WHERE year=%s AND month=%s AND day=%s"
            val = (year, month, day)
            self.dbWrapper.dbCursor.execute(query, val)
            myresult = self.dbWrapper.dbCursor.fetchone()

            if myresult:
                return self.getDayByID(myresult[0])
            return None

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            self.dbWrapper.updateOwnClassVars()
            return self.getDayByDate(year, month, day, True)

    def createNewDay(self, year: int, month: int, day: int, alreadyAttemptedToUpdateOwnClassVars: bool = False) -> dict or None:
        """
        Creates a new day entry in the database if it doesn't already exist.

        Args:
            year (int): The year of the day entry.
            month (int): The month of the day entry.
            day (int): The day of the day entry.
            alreadyAttemptedToUpdateOwnClassVars (bool): Flag to prevent multiple updates in case of error.

        Returns:
            dict or None: A dictionary containing the created or existing day details, or None if it fails.
        """
        try:
            existing_day = self.getDayByDate(year, month, day)
            if existing_day:
                return existing_day

            query = "INSERT INTO days (year, month, day) VALUES (%s, %s, %s)"
            val = (year, month, day)
            self.dbWrapper.dbCursor.execute(query, val)
            self.dbWrapper.dbConnection.commit()

            return self.getDayByID(self.dbWrapper.dbCursor.lastrowid)

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            self.dbWrapper.updateOwnClassVars()
            return self.createNewDay(year, month, day, True)
