from credentialsItem import CredentialsItem


# Json model of a valid DeleteMealItem to send to the api.
# {
#     "credentials": {
#         "token": "XXXX",
#         "userName": "DemoUser123",
#         "hashedPassword": "XXXX"
#     },
#     "year": 2024,
#     "month": 10,
#     "day": 12,
#     "mealType": "lunch",
# }


class DeleteMealItem:

    # Constructor.
    def __init__(self, credentialsItem: CredentialsItem, year, month, day, mealType):
        self.credentialsItem = credentialsItem
        self.year = year
        self.month = month
        self.day = day
        self.mealType = mealType

    def toString(self):
        classAsString = 'DeleteMealItem{'
        classAsString += '"credentials":"' + str(self.credentialsItem.toString()) + '", '
        classAsString += '"year":' + str(self.year) + ', '
        classAsString += '"month":' + str(self.month) + ', '
        classAsString += '"day":' + str(self.day) + ', '
        classAsString += '"mealType":"' + str(self.mealType) + '}'

        return classAsString
