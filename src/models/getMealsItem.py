from credentialsItem import CredentialsItem

class GetMealsItem:
    """
    Model used to wrap the details for getting meals sent to the API.

    Json model of a valid GetMealsItem to send to the API:
    {
        "credentials": {
            "token": "<your_actual_token_here>",
            "userName": "<your_actual_username_here>",
            "hashedPassword": "<your_actual_hashed_password_here>"
        },
        "year": 2024,
        "month": 10,
        "day": 12
    }

    Attributes:
        credentialsItem (CredentialsItem): The credentials of the user.
        year (int): The year of the meal entry to retrieve.
        month (int): The month of the meal entry to retrieve.
        day (int): The day of the meal entry to retrieve.
    """

    def __init__(self, credentialsItem: CredentialsItem, year: int, month: int, day: int):
        """
        Initializes the GetMealsItem with credentials, year, month, and day.

        Args:
            credentialsItem (CredentialsItem): The credentials of the user.
            year (int): The year of the meal entry to retrieve.
            month (int): The month of the meal entry to retrieve.
            day (int): The day of the meal entry to retrieve.
        """
        self.credentialsItem = credentialsItem
        self.year = year
        self.month = month
        self.day = day

    def __str__(self) -> str:
        """
        Returns a string representation of the GetMealsItem.

        Returns:
            str: A formatted string representation of the GetMealsItem.
        """
        class_as_string = 'GetMealsItem{'
        class_as_string += f'"credentials": "{self.credentialsItem}", '
        class_as_string += f'"year": {self.year}, '
        class_as_string += f'"month": {self.month}, '
        class_as_string += f'"day": {self.day}'
        class_as_string += '}'

        return class_as_string
