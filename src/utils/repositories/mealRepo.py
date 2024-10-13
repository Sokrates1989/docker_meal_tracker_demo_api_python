# mealRepo.py
class MealRepo:

    def __init__(self, dbWrapper):
        self.dbWrapper = dbWrapper

    def getMealByID(self, mealID, alreadyAttemptedToUpdateOwnClassVars=False):
        try:
            query = "SELECT ID, fat_level, sugar_level FROM meals WHERE ID=%s"
            val = (mealID,)
            self.dbWrapper.dbCursor.execute(query, val)
            myresult = self.dbWrapper.dbCursor.fetchone()

            meal = None
            if myresult is not None:
                meal = {
                    'ID': myresult[0],
                    'fat_level': myresult[1],
                    'sugar_level': myresult[2],
                }
            return meal

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            else:
                self.dbWrapper.updateOwnClassVars()
                return self.dbWrapper.getMealRepo().getMealByID(mealID, True)

    def createNewMeal(self, fat_level, sugar_level, alreadyAttemptedToUpdateOwnClassVars=False):
        try:
            query = "INSERT INTO meals (fat_level, sugar_level) VALUES (%s, %s)"
            val = (fat_level, sugar_level)
            self.dbWrapper.dbCursor.execute(query, val)
            self.dbWrapper.dbConnection.commit()

            return self.getMealByID(self.dbWrapper.dbCursor.lastrowid)

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            else:
                self.dbWrapper.updateOwnClassVars()
                return self.dbWrapper.getMealRepo().createNewMeal(fat_level, sugar_level, True)



    def updateMeal(self, mealID, fat_level, sugar_level, alreadyAttemptedToUpdateOwnClassVars=False):
        """Update the fat and sugar levels of an existing meal in the database."""
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
            else:
                self.dbWrapper.updateOwnClassVars()
                return self.dbWrapper.getMealRepo().updateMeal(mealID, fat_level, sugar_level, True)
            
    
    def deleteMeal(self, userID, dayID, mealTypeID, mealID, alreadyAttemptedToUpdateOwnClassVars=False):
        """Delete a meal and its corresponding entry in day_meals."""
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
            else:
                self.dbWrapper.updateOwnClassVars()
                return self.deleteMeal(userID, dayID, mealTypeID, mealID, True)
