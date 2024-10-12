# mealTypeRepo.py
class MealTypeRepo:

    def __init__(self, dbWrapper):
        self.dbWrapper = dbWrapper

    def getMealTypeIDByName(self, mealTypeName, alreadyAttemptedToUpdateOwnClassVars=False):
        try:
            query = "SELECT ID FROM meal_types WHERE name = %s"
            val = (mealTypeName,)
            self.dbWrapper.dbCursor.execute(query, val)
            myresult = self.dbWrapper.dbCursor.fetchone()
            if myresult is not None:
                return myresult[0]
            else:
                return None

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            else:
                self.dbWrapper.updateOwnClassVars()
                return self.dbWrapper.getMealTypeRepo().getMealTypeIDByName(mealTypeName, True)

    def getMealTypeNameByID(self, mealTypeID, alreadyAttemptedToUpdateOwnClassVars=False):
        try:
            query = "SELECT name FROM meal_types WHERE ID = %s"
            val = (mealTypeID,)
            self.dbWrapper.dbCursor.execute(query, val)
            myresult = self.dbWrapper.dbCursor.fetchone()
            if myresult is not None:
                return myresult[0]
            else:
                return None

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            else:
                self.dbWrapper.updateOwnClassVars()
                return self.dbWrapper.getMealTypeRepo().getMealTypeNameByID(mealTypeID, True)
            

    def getAllMealTypes(self):
        try:
            query = "SELECT ID, name FROM meal_types ORDER BY ID"
            self.dbWrapper.dbCursor.execute(query)
            myresults = self.dbWrapper.dbCursor.fetchall()

            mealTypes = []
            for result in myresults:
                mealTypes.append({
                    'ID': result[0],
                    'name': result[1]
                })

            return mealTypes

        except Exception as e:
            print(f"Error fetching meal types: {e}")
            return None

