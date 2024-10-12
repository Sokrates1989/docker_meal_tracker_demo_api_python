import mysql.connector

# dayMealRepo.py
class DayMealRepo:

    def __init__(self, dbWrapper):
        self.dbWrapper = dbWrapper

    def getDayMeal(self, userID, dayID, mealTypeID, alreadyAttemptedToUpdateOwnClassVars=False):
        try:
            query = """
                SELECT fk_user_id, fk_day_id, fk_meal_type_id, fk_meal_id
                FROM day_meals
                WHERE fk_user_id=%s AND fk_day_id=%s AND fk_meal_type_id=%s
            """
            val = (userID, dayID, mealTypeID)
            self.dbWrapper.dbCursor.execute(query, val)
            myresult = self.dbWrapper.dbCursor.fetchone()

            if myresult is not None:
                dayMeal = {
                    'fk_user_id': myresult[0],
                    'fk_day_id': myresult[1],
                    'fk_meal_type_id': myresult[2],
                    'fk_meal_id': myresult[3],
                }
                return dayMeal
            else:
                return None

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            else:
                self.dbWrapper.updateOwnClassVars()
                return self.dbWrapper.getDayMealRepo().getDayMeal(userID, dayID, mealTypeID, True)

    def createNewDayMeal(self, userID, dayID, mealTypeID, mealID, alreadyAttemptedToUpdateOwnClassVars=False):
        try:
            query = """
                INSERT INTO day_meals (fk_user_id, fk_day_id, fk_meal_type_id, fk_meal_id)
                VALUES (%s, %s, %s, %s)
            """
            val = (userID, dayID, mealTypeID, mealID)
            self.dbWrapper.dbCursor.execute(query, val)
            self.dbWrapper.dbConnection.commit()

            return self.getDayMeal(userID, dayID, mealTypeID)

        except mysql.connector.IntegrityError as e:
            return None

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            else:
                self.dbWrapper.updateOwnClassVars()
                return self.dbWrapper.getDayMealRepo().createNewDayMeal(userID, dayID, mealTypeID, mealID, True)

    def getDayMealsByUserIDAndDayID(self, userID, dayID, alreadyAttemptedToUpdateOwnClassVars=False):
        try:
            query = """
                SELECT fk_meal_type_id, fk_meal_id
                FROM day_meals
                WHERE fk_user_id=%s AND fk_day_id=%s
            """
            val = (userID, dayID)
            self.dbWrapper.dbCursor.execute(query, val)
            myresults = self.dbWrapper.dbCursor.fetchall()

            dayMeals = []
            for result in myresults:
                dayMeals.append({
                    'fk_meal_type_id': result[0],
                    'fk_meal_id': result[1],
                })
            return dayMeals

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return []
            else:
                self.dbWrapper.updateOwnClassVars()
                return self.dbWrapper.getDayMealRepo().getDayMealsByUserIDAndDayID(userID, dayID, True)
