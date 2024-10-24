# Copyright (C) 2024 Patrick Michiels
# All rights reserved.
# This source code is licensed under the Evaluation License Agreement and
# may not be used, modified, or distributed without explicit permission from the author.
# This code is provided for evaluation purposes only.

from src.models.credentialsItem import CredentialsItem

class DeleteMealItem:
    """
    Model used to wrap the details for deleting a meal sent to the API.

    Json model of a valid DeleteMealItem to send to the API:
    {
        "credentials": {
            "token": "<your_actual_token_here>",
            "userName": "<your_actual_username_here>",
            "hashedPassword": "<your_actual_hashed_password_here>"
        },
        "year": 2024,
        "month": 10,
        "day": 12,
        "mealType": "lunch"
    }

    Attributes:
        credentialsItem (CredentialsItem): The credentials of the user.
        year (int): The year of the meal entry to delete.
        month (int): The month of the meal entry to delete.
        day (int): The day of the meal entry to delete.
        mealType (str): The type of meal (e.g., "breakfast", "lunch", "dinner", "snacks").
    """

    def __init__(self, credentialsItem: CredentialsItem, year: int, month: int, day: int, mealType: str):
        """
        Initializes the DeleteMealItem with credentials, year, month, day, and mealType.

        Args:
            credentialsItem (CredentialsItem): The credentials of the user.
            year (int): The year of the meal entry to delete.
            month (int): The month of the meal entry to delete.
            day (int): The day of the meal entry to delete.
            mealType (str): The type of meal (e.g., "breakfast", "lunch", "dinner", "snacks").
        """
        self.credentialsItem = credentialsItem
        self.year = year
        self.month = month
        self.day = day
        self.mealType = mealType

    def __str__(self) -> str:
        """
        Returns a string representation of the DeleteMealItem.

        Returns:
            str: A formatted string representation of the DeleteMealItem.
        """
        class_as_string = 'DeleteMealItem{'
        class_as_string += f'"credentials": "{self.credentialsItem}", '
        class_as_string += f'"year": {self.year}, '
        class_as_string += f'"month": {self.month}, '
        class_as_string += f'"day": {self.day}, '
        class_as_string += f'"mealType": "{self.mealType}"'
        class_as_string += '}'

        return class_as_string
