# Copyright (C) 2024 Patrick Michiels
# All rights reserved.
# This source code is licensed under the Evaluation License Agreement and
# may not be used, modified, or distributed without explicit permission from the author.
# This code is provided for evaluation purposes only.

class MealTypeRepo:
    """
    Repository class for managing meal type records in the database.

    This class provides methods to retrieve meal type entries based on their ID or name,
    and to fetch all available meal types.
    
    Attributes:
        dbWrapper: The database wrapper that provides database connection and cursor.
    """

    def __init__(self, dbWrapper):
        """
        Initializes the MealTypeRepo with a database wrapper.

        Args:
            dbWrapper: The database wrapper object used to interact with the database.
        """
        self.dbWrapper = dbWrapper

    def getMealTypeIDByName(self, mealTypeName: str, alreadyAttemptedToUpdateOwnClassVars: bool = False) -> int or None:
        """
        Retrieves the meal type ID by the meal type name.

        Args:
            mealTypeName (str): The name of the meal type.
            alreadyAttemptedToUpdateOwnClassVars (bool): Flag to prevent multiple updates in case of error.

        Returns:
            int or None: The meal type ID if found, otherwise None.
        """
        try:
            query = "SELECT ID FROM meal_types WHERE name = %s"
            val = (mealTypeName,)
            self.dbWrapper.dbCursor.execute(query, val)
            myresult = self.dbWrapper.dbCursor.fetchone()
            
            if myresult:
                return myresult[0]
            return None

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            self.dbWrapper.updateOwnClassVars()
            return self.getMealTypeIDByName(mealTypeName, True)

    def getMealTypeNameByID(self, mealTypeID: int, alreadyAttemptedToUpdateOwnClassVars: bool = False) -> str or None:
        """
        Retrieves the meal type name by the meal type ID.

        Args:
            mealTypeID (int): The ID of the meal type.
            alreadyAttemptedToUpdateOwnClassVars (bool): Flag to prevent multiple updates in case of error.

        Returns:
            str or None: The meal type name if found, otherwise None.
        """
        try:
            query = "SELECT name FROM meal_types WHERE ID = %s"
            val = (mealTypeID,)
            self.dbWrapper.dbCursor.execute(query, val)
            myresult = self.dbWrapper.dbCursor.fetchone()
            
            if myresult:
                return myresult[0]
            return None

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            self.dbWrapper.updateOwnClassVars()
            return self.getMealTypeNameByID(mealTypeID, True)

    def getAllMealTypes(self) -> list or None:
        """
        Retrieves all meal types from the database.

        Returns:
            list or None: A list of dictionaries containing the meal type IDs and names, or None if an error occurs.
        """
        try:
            query = "SELECT ID, name FROM meal_types ORDER BY ID"
            self.dbWrapper.dbCursor.execute(query)
            myresults = self.dbWrapper.dbCursor.fetchall()

            mealTypes = [{'ID': result[0], 'name': result[1]} for result in myresults]

            return mealTypes

        except Exception as e:
            print(f"Error fetching meal types: {e}")
            return None
