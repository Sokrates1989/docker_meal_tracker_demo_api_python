# Copyright (C) 2024 Patrick Michiels
# All rights reserved.
# This source code is licensed under the Evaluation License Agreement and
# may not be used, modified, or distributed without explicit permission from the author.
# This code is provided for evaluation purposes only.

class CredentialsItem:
    """
    Model used to wrap user credentials sent to the API to use globally.

    Attributes:
        token (str): The authentication token sent by the user.
        userName (str): The username of the user.
        hashedPassword (str): The hashed password of the user.
    """

    def __init__(self, token: str, userName: str, hashedPassword: str):
        """
        Initializes the CredentialsItem with token, userName, and hashedPassword.

        Args:
            token (str): The authentication token sent by the user.
            userName (str): The username of the user.
            hashedPassword (str): The hashed password of the user.
        """
        self.token = token
        self.userName = userName
        self.hashedPassword = hashedPassword

    def __str__(self) -> str:
        """
        Returns a string representation of the CredentialsItem, 
        displaying only the first and last three characters of the token and hashed password for security reasons.

        Returns:
            str: A formatted string representation of the CredentialsItem.
        """
        token_length = len(self.token)
        hashed_password_length = len(self.hashedPassword)

        class_as_string = 'CredentialsItem{'
        
        # Handle token display
        if token_length < 3:
            class_as_string += f'"token":INVALID_LENGTH---PASSED:"{self.token}", '
        else:
            class_as_string += f'"token":"{self.token[:3]}---XXX---{self.token[-3:]}", '
        
        # Handle userName display
        class_as_string += f'"userName":"{self.userName}", '

        # Handle hashedPassword display
        if hashed_password_length < 3:
            class_as_string += f'"hashedPassword":INVALID_LENGTH---PASSED:"{self.hashedPassword}", '
        else:
            class_as_string += f'"hashedPassword":"{self.hashedPassword[:3]}---XXX---{self.hashedPassword[-3:]}", '

        # Remove the trailing comma and space if present
        if class_as_string.endswith(", "):
            class_as_string = class_as_string[:-2]

        class_as_string += '}'

        return class_as_string
