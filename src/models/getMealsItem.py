# getMealsItem.py
from credentialsItem import CredentialsItem

class GetMealsItem:

    # Constructor.
    def __init__(self, credentialsItem: CredentialsItem, year, month, day):
        self.credentialsItem = credentialsItem
        self.year = year
        self.month = month
        self.day = day

    def toString(self):
        classAsString = 'GetMealsItem{'
        classAsString += '"credentials":"' + str(self.credentialsItem.toString()) + '", '
        classAsString += '"year":' + str(self.year) + ', '
        classAsString += '"month":' + str(self.month) + ', '
        classAsString += '"day":' + str(self.day) + '}'

        return classAsString
