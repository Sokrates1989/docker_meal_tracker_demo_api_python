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
