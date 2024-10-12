from credentialsItem import CredentialsItem

class MealItem:

    # Constructor.
    def __init__(self, credentialsItem: CredentialsItem, year, month, day, mealType, fat_level, sugar_level):
        self.credentialsItem = credentialsItem
        self.year = year
        self.month = month
        self.day = day
        self.mealType = mealType
        self.fat_level = fat_level
        self.sugar_level = sugar_level

    def toString(self):
        classAsString = 'MealItem{'
        classAsString += '"credentials":"' + str(self.credentialsItem.toString()) + '", '
        classAsString += '"year":' + str(self.year) + ', '
        classAsString += '"month":' + str(self.month) + ', '
        classAsString += '"day":' + str(self.day) + ', '
        classAsString += '"mealType":"' + str(self.mealType) + '", '
        classAsString += '"fat_level":' + str(self.fat_level) + ', '
        classAsString += '"sugar_level":' + str(self.sugar_level) + '}'

        return classAsString
