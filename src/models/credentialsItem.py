class CredentialsItem:
    """
    Model used to wrap user credentials sent to the API.

    Json model of a valid CredentialsItem to send to the API:
    {
      "token": "<your_actual_token_here>",
      "userName": "<your_actual_username_here>",
      "hashedPassword": "<your_actual_hashed_password_here>"
    }

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
