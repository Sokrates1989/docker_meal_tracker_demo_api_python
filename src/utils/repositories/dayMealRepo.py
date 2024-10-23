import mysql.connector

class DayMealRepo:
    """
    Repository class for managing day meal records in the database.

    This class provides methods to retrieve and create day meal entries associated with a user and specific days.

    Attributes:
        dbWrapper: The database wrapper that provides database connection and cursor.
    """

    def __init__(self, dbWrapper):
        """
        Initializes the DayMealRepo with a database wrapper.

        Args:
            dbWrapper: The database wrapper object used to interact with the database.
        """
        self.dbWrapper = dbWrapper

    def getDayMeal(self, userID: int, dayID: int, mealTypeID: int, alreadyAttemptedToUpdateOwnClassVars: bool = False):
        """
        Retrieves a day meal for a given user, day, and meal type from the database.

        Args:
            userID (int): The ID of the user.
            dayID (int): The ID of the day.
            mealTypeID (int): The ID of the meal type.
            alreadyAttemptedToUpdateOwnClassVars (bool): Flag to prevent multiple updates in case of error.

        Returns:
            dict or None: A dictionary containing the day meal details if found, otherwise None.
        """
        try:
            query = """
                SELECT fk_user_id, fk_day_id, fk_meal_type_id, fk_meal_id
                FROM day_meals
                WHERE fk_user_id=%s AND fk_day_id=%s AND fk_meal_type_id=%s
            """
            val = (userID, dayID, mealTypeID)
            self.dbWrapper.dbCursor.execute(query, val)
            myresult = self.dbWrapper.dbCursor.fetchone()

            if myresult:
                return {
                    'fk_user_id': myresult[0],
                    'fk_day_id': myresult[1],
                    'fk_meal_type_id': myresult[2],
                    'fk_meal_id': myresult[3],
                }
            return None

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            self.dbWrapper.updateOwnClassVars()
            return self.getDayMeal(userID, dayID, mealTypeID, True)

    def createNewDayMeal(self, userID: int, dayID: int, mealTypeID: int, mealID: int, alreadyAttemptedToUpdateOwnClassVars: bool = False):
        """
        Creates a new day meal entry in the database.

        Args:
            userID (int): The ID of the user.
            dayID (int): The ID of the day.
            mealTypeID (int): The ID of the meal type.
            mealID (int): The ID of the meal.
            alreadyAttemptedToUpdateOwnClassVars (bool): Flag to prevent multiple updates in case of error.

        Returns:
            dict or None: A dictionary containing the created day meal details, or None if it fails.
        """
        try:
            query = """
                INSERT INTO day_meals (fk_user_id, fk_day_id, fk_meal_type_id, fk_meal_id)
                VALUES (%s, %s, %s, %s)
            """
            val = (userID, dayID, mealTypeID, mealID)
            self.dbWrapper.dbCursor.execute(query, val)
            self.dbWrapper.dbConnection.commit()

            return self.getDayMeal(userID, dayID, mealTypeID)

        except mysql.connector.IntegrityError:
            return None

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            self.dbWrapper.updateOwnClassVars()
            return self.createNewDayMeal(userID, dayID, mealTypeID, mealID, True)

    def getDayMealsByUserIDAndDayID(self, userID: int, dayID: int, alreadyAttemptedToUpdateOwnClassVars: bool = False):
        """
        Retrieves all day meals for a given user and day from the database.

        Args:
            userID (int): The ID of the user.
            dayID (int): The ID of the day.
            alreadyAttemptedToUpdateOwnClassVars (bool): Flag to prevent multiple updates in case of error.

        Returns:
            list: A list of dictionaries containing meal type ID and meal ID for each day meal.
        """
        try:
            query = """
                SELECT fk_meal_type_id, fk_meal_id
                FROM day_meals
                WHERE fk_user_id=%s AND fk_day_id=%s
            """
            val = (userID, dayID)
            self.dbWrapper.dbCursor.execute(query, val)
            myresults = self.dbWrapper.dbCursor.fetchall()

            dayMeals = [{'fk_meal_type_id': result[0], 'fk_meal_id': result[1]} for result in myresults]
            return dayMeals

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return []
            self.dbWrapper.updateOwnClassVars()
            return self.getDayMealsByUserIDAndDayID(userID, dayID, True)
