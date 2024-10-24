# Copyright (C) 2024 Patrick Michiels
# All rights reserved.
# This source code is licensed under the Evaluation License Agreement and
# may not be used, modified, or distributed without explicit permission from the author.
# This code is provided for evaluation purposes only.

class AuthenticationItem:
    """
    Model used to wrap authentication settings sent to the API.

    Json model of a valid AuthenticationItem to send to the API:
    {
      "token": "<your_actual_token_here>"
    }

    Attributes:
        token (str): The authentication token sent by the user.
    """

    def __init__(self, token: str):
        """
        Initializes the AuthenticationItem with a token.

        Args:
            token (str): The authentication token sent by the user.
        """
        self.token = token

    def __str__(self) -> str:
        """
        Returns a string representation of the AuthenticationItem, 
        displaying only the first and last three characters of the token for security reasons.

        Returns:
            str: A formatted string representation of the AuthenticationItem.
        """
        token_length = len(self.token)

        class_as_string = 'AuthenticationItem{'
        if token_length < 3:
            class_as_string += f'"token":INVALID_LENGTH---PASSED:"{self.token}"'
        else:
            class_as_string += f'"token":"{self.token[:3]}---XXX---{self.token[-3:]}"'
        class_as_string += '}'

        return class_as_string
