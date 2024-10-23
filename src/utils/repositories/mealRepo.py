class MealRepo:
    """
    Repository class for managing meal records in the database.

    This class provides methods to retrieve, create, update, and delete meal entries.
    
    Attributes:
        dbWrapper: The database wrapper that provides database connection and cursor.
    """

    def __init__(self, dbWrapper):
        """
        Initializes the MealRepo with a database wrapper.

        Args:
            dbWrapper: The database wrapper object used to interact with the database.
        """
        self.dbWrapper = dbWrapper

    def getMealByID(self, mealID: int, alreadyAttemptedToUpdateOwnClassVars: bool = False) -> dict or None:
        """
        Retrieves a meal entry by its ID from the database.

        Args:
            mealID (int): The ID of the meal.
            alreadyAttemptedToUpdateOwnClassVars (bool): Flag to prevent multiple updates in case of error.

        Returns:
            dict or None: A dictionary containing the meal details if found, otherwise None.
        """
        try:
            query = "SELECT ID, fat_level, sugar_level FROM meals WHERE ID=%s"
            val = (mealID,)
            self.dbWrapper.dbCursor.execute(query, val)
            myresult = self.dbWrapper.dbCursor.fetchone()

            if myresult:
                meal = {
                    'ID': myresult[0],
                    'fat_level': myresult[1],
                    'sugar_level': myresult[2],
                }
                return meal
            return None

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            self.dbWrapper.updateOwnClassVars()
            return self.getMealByID(mealID, True)

    def createNewMeal(self, fat_level: int, sugar_level: int, alreadyAttemptedToUpdateOwnClassVars: bool = False) -> dict or None:
        """
        Creates a new meal entry in the database.

        Args:
            fat_level (int): The fat level of the meal (0: Low, 1: Medium, 2: High).
            sugar_level (int): The sugar level of the meal (0: Low, 1: Medium, 2: High).
            alreadyAttemptedToUpdateOwnClassVars (bool): Flag to prevent multiple updates in case of error.

        Returns:
            dict or None: A dictionary containing the created meal details, or None if it fails.
        """
        try:
            query = "INSERT INTO meals (fat_level, sugar_level) VALUES (%s, %s)"
            val = (fat_level, sugar_level)
            self.dbWrapper.dbCursor.execute(query, val)
            self.dbWrapper.dbConnection.commit()

            return self.getMealByID(self.dbWrapper.dbCursor.lastrowid)

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            self.dbWrapper.updateOwnClassVars()
            return self.createNewMeal(fat_level, sugar_level, True)

    def updateMeal(self, mealID: int, fat_level: int, sugar_level: int, alreadyAttemptedToUpdateOwnClassVars: bool = False) -> bool or None:
        """
        Updates the fat and sugar levels of an existing meal in the database.

        Args:
            mealID (int): The ID of the meal.
            fat_level (int): The updated fat level of the meal (0: Low, 1: Medium, 2: High).
            sugar_level (int): The updated sugar level of the meal (0: Low, 1: Medium, 2: High).
            alreadyAttemptedToUpdateOwnClassVars (bool): Flag to prevent multiple updates in case of error.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            query = """
            UPDATE meals
            SET fat_level = %s, sugar_level = %s
            WHERE ID = %s
            """
            val = (fat_level, sugar_level, mealID)
            self.dbWrapper.dbCursor.execute(query, val)
            self.dbWrapper.dbConnection.commit()

            return True

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            self.dbWrapper.updateOwnClassVars()
            return self.updateMeal(mealID, fat_level, sugar_level, True)

    def deleteMeal(self, userID: int, dayID: int, mealTypeID: int, mealID: int, alreadyAttemptedToUpdateOwnClassVars: bool = False) -> bool or None:
        """
        Deletes a meal and its corresponding entry in the day_meals table.

        Args:
            userID (int): The ID of the user.
            dayID (int): The ID of the day entry.
            mealTypeID (int): The ID of the meal type entry.
            mealID (int): The ID of the meal entry to be deleted.
            alreadyAttemptedToUpdateOwnClassVars (bool): Flag to prevent multiple updates in case of error.

        Returns:
            bool or None: True if the meal and day_meals entries were deleted successfully, 
                          False if the day_meals entry was not found, 
                          None if the operation fails.
        """
        try:
            # Delete entry from day_meals
            query_day_meals = """
                DELETE FROM day_meals 
                WHERE fk_user_id = %s AND fk_day_id = %s AND fk_meal_type_id = %s
            """
            val_day_meals = (userID, dayID, mealTypeID)
            self.dbWrapper.dbCursor.execute(query_day_meals, val_day_meals)
            
            if self.dbWrapper.dbCursor.rowcount == 0:
                return False  # day_meals entry not found

            # Now delete the meal from meals
            query_meal = "DELETE FROM meals WHERE ID = %s"
            val_meal = (mealID,)
            self.dbWrapper.dbCursor.execute(query_meal, val_meal)
            self.dbWrapper.dbConnection.commit()

            return True  # Deletion successful

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            self.dbWrapper.updateOwnClassVars()
            return self.deleteMeal(userID, dayID, mealTypeID, mealID, True)
