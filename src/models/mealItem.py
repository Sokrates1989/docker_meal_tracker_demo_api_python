from src.models.credentialsItem import CredentialsItem

class MealItem:
    """
    Model used to wrap the details for a meal sent to the API.

    Json model of a valid MealItem to send to the API:
    {
        "credentials": {
            "token": "<your_actual_token_here>",
            "userName": "<your_actual_username_here>",
            "hashedPassword": "<your_actual_hashed_password_here>"
        },
        "year": 2024,
        "month": 10,
        "day": 12,
        "mealType": "lunch",
        "fat_level": 1,
        "sugar_level": 2
    }

    Attributes:
        credentialsItem (CredentialsItem): The credentials of the user.
        year (int): The year of the meal entry.
        month (int): The month of the meal entry.
        day (int): The day of the meal entry.
        mealType (str): The type of meal (e.g., "breakfast", "lunch", "dinner", "snacks").
        fat_level (int): The fat level of the meal (0: Low, 1: Medium, 2: High).
        sugar_level (int): The sugar level of the meal (0: Low, 1: Medium, 2: High).
    """

    def __init__(self, credentialsItem: CredentialsItem, year: int, month: int, day: int, mealType: str, fat_level: int, sugar_level: int):
        """
        Initializes the MealItem with credentials, year, month, day, mealType, fat_level, and sugar_level.

        Args:
            credentialsItem (CredentialsItem): The credentials of the user.
            year (int): The year of the meal entry.
            month (int): The month of the meal entry.
            day (int): The day of the meal entry.
            mealType (str): The type of meal (e.g., "breakfast", "lunch", "dinner", "snacks").
            fat_level (int): The fat level of the meal (0: Low, 1: Medium, 2: High).
            sugar_level (int): The sugar level of the meal (0: Low, 1: Medium, 2: High).
        """
        self.credentialsItem = credentialsItem
        self.year = year
        self.month = month
        self.day = day
        self.mealType = mealType
        self.fat_level = fat_level
        self.sugar_level = sugar_level

    def __str__(self) -> str:
        """
        Returns a string representation of the MealItem.

        Returns:
            str: A formatted string representation of the MealItem.
        """
        class_as_string = 'MealItem{'
        class_as_string += f'"credentials": "{self.credentialsItem}", '
        class_as_string += f'"year": {self.year}, '
        class_as_string += f'"month": {self.month}, '
        class_as_string += f'"day": {self.day}, '
        class_as_string += f'"mealType": "{self.mealType}", '
        class_as_string += f'"fat_level": {self.fat_level}, '
        class_as_string += f'"sugar_level": {self.sugar_level}'
        class_as_string += '}'

        return class_as_string
