# dayRepo.py
class DayRepo:

    def __init__(self, dbWrapper):
        self.dbWrapper = dbWrapper

    def getDayByID(self, dayID, alreadyAttemptedToUpdateOwnClassVars=False):
        try:
            query = "SELECT ID, year, month, day FROM days WHERE ID=%s"
            val = (dayID,)
            self.dbWrapper.dbCursor.execute(query, val)
            myresult = self.dbWrapper.dbCursor.fetchone()

            day = None
            if myresult is not None:
                day = {
                    'ID': myresult[0],
                    'year': myresult[1],
                    'month': myresult[2],
                    'day': myresult[3]
                }
            return day

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            else:
                self.dbWrapper.updateOwnClassVars()
                return self.dbWrapper.getDayRepo().getDayByID(dayID, True)

    def getDayByDate(self, year, month, day, alreadyAttemptedToUpdateOwnClassVars=False):
        try:
            query = "SELECT ID FROM days WHERE year=%s AND month=%s AND day=%s"
            val = (year, month, day)
            self.dbWrapper.dbCursor.execute(query, val)
            myresult = self.dbWrapper.dbCursor.fetchone()

            if myresult is not None:
                return self.getDayByID(myresult[0])
            else:
                return None

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            else:
                self.dbWrapper.updateOwnClassVars()
                return self.dbWrapper.getDayRepo().getDayByDate(year, month, day, True)

    def createNewDay(self, year, month, day, alreadyAttemptedToUpdateOwnClassVars=False):
        try:
            existing_day = self.getDayByDate(year, month, day)
            if existing_day is not None:
                return existing_day

            query = "INSERT INTO days (year, month, day) VALUES (%s, %s, %s)"
            val = (year, month, day)
            self.dbWrapper.dbCursor.execute(query, val)
            self.dbWrapper.dbConnection.commit()

            return self.getDayByID(self.dbWrapper.dbCursor.lastrowid)

        except Exception as e:
            if alreadyAttemptedToUpdateOwnClassVars:
                return None
            else:
                self.dbWrapper.updateOwnClassVars()
                return self.dbWrapper.getDayRepo().createNewDay(year, month, day, True)
